from typing import List, Dict, Any

from .rag import rag_query

# Simple in-memory todo list (per process)
TODO_LIST: List[str] = []


def tool_search_documents(query: str) -> str:
    return rag_query(query, k=5)


def tool_calculate_expression(expression: str) -> str:
    try:
        # NOTE: eval is dangerous in real life; here it's sandboxed (no builtins)
        result = eval(expression, {"__builtins__": {}})
        return f"Result: {result}"
    except Exception as e:
        return f"Error evaluating expression: {e}"


def tool_manage_todos(action: str, item: str | None = None) -> str:
    global TODO_LIST
    if action == "add" and item:
        TODO_LIST.append(item)
        return f"✅ Added todo: {item}"
    elif action == "list":
        if not TODO_LIST:
            return "Your todo list is empty."
        return "Your todos:\n" + "\n".join(f"{i+1}. {t}" for i, t in enumerate(TODO_LIST))
    elif action == "remove" and item:
        if item in TODO_LIST:
            TODO_LIST.remove(item)
            return f"🗑️ Removed todo: {item}"
        else:
            return f"Todo not found: {item}"
    else:
        return "Invalid action or missing item."


# --- Tool schema for Gemini ---

TOOLS_SPEC = [
    {
        "name": "search_documents",
        "description": "Search in the uploaded documents and return relevant passages.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "User question related to uploaded documents.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "calculate_expression",
        "description": "Evaluate a mathematical expression and return the result.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression like '5 * (2 + 3)'",
                }
            },
            "required": ["expression"],
        },
    },
    {
        "name": "manage_todos",
        "description": "Add, list, or remove tasks from a todo list.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["add", "list", "remove"],
                    "description": "Which operation to perform.",
                },
                "item": {
                    "type": "string",
                    "description": "Todo text (needed for add/remove).",
                },
            },
            "required": ["action"],
        },
    },
]


def call_tool(name: str, arguments: Dict[str, Any]) -> str:
    if name == "search_documents":
        return tool_search_documents(**arguments)
    elif name == "calculate_expression":
        return tool_calculate_expression(**arguments)
    elif name == "manage_todos":
        return tool_manage_todos(**arguments)
    else:
        return f"Unknown tool: {name}"
