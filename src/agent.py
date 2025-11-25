import json
from typing import Dict, Any, Optional

from .gemini_client import get_chat_model
from .tools import TOOLS_SPEC, call_tool

# Wrap the tool definitions as expected by google-generativeai
TOOLS_WRAPPED = [{"function_declarations": TOOLS_SPEC}]


def _extract_function_call(resp) -> Optional[Any]:
    """Safely get the first function_call part from the response, if any."""
    if not getattr(resp, "candidates", None):
        return None
    candidate = resp.candidates[0]
    if not candidate.content or not candidate.content.parts:
        return None

    for p in candidate.content.parts:
        fc = getattr(p, "function_call", None)
        if fc:
            return fc
    return None


def _safe_text(resp) -> str:
    """Safely extract text from a Gemini response."""
    try:
        return resp.text
    except Exception:
        if getattr(resp, "candidates", None) and resp.candidates[0].content.parts:
            texts = []
            for p in resp.candidates[0].content.parts:
                if getattr(p, "text", None):
                    texts.append(p.text)
            return " ".join(texts) if texts else "No response text."
        return "No response text."


def run_agent(user_message: str) -> Dict[str, Optional[str]]:
    """
    1️⃣ Call Gemini with tools and user message.
    2️⃣ If Gemini asks to call a tool, execute it.
    3️⃣ Send a function_response back to Gemini with the tool result.
    4️⃣ Return the final answer + tool info.
    """
    model = get_chat_model(tools=TOOLS_WRAPPED)

    # 1) First call: user → model (may contain function_call)
    first_resp = model.generate_content(
        contents=[{"role": "user", "parts": [{"text": user_message}]}]
    )

    tool_name: Optional[str] = None
    tool_output: Optional[str] = None

    function_call = _extract_function_call(first_resp)

    # If no function call, just return the text
    if not function_call:
        final_answer = _safe_text(first_resp)
        return {
            "answer": final_answer,
            "tool_name": None,
            "tool_output": None,
        }

    # 2) Execute the requested tool
    tool_name = function_call.name
    args = dict(function_call.args) if function_call.args is not None else {}
    tool_output = call_tool(tool_name, args)

    # 3) Build a proper function_response turn for the tool
    tool_response_turn = {
        "role": "tool",
        "parts": [
            {
                "function_response": {
                    "name": tool_name,
                    "response": {
                        "result": tool_output,
                        "arguments": args,
                    },
                }
            }
        ],
    }

    # 4) Second call: send the FULL conversation in the correct order
    # user -> model(function_call) -> tool(function_response)
    second_resp = model.generate_content(
        contents=[
            {"role": "user", "parts": [{"text": user_message}]},
            first_resp.candidates[0].content,   # model turn with function_call
            tool_response_turn,                 # tool turn with function_response
        ]
    )

    final_answer = _safe_text(second_resp)

    return {
        "answer": final_answer,
        "tool_name": tool_name,
        "tool_output": tool_output,
    }
