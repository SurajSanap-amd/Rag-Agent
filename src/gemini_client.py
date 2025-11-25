import google.generativeai as genai
from .config import get_gemini_api_key

_api_key = get_gemini_api_key()
genai.configure(api_key=_api_key)

EMBED_MODEL = "models/text-embedding-004"
CHAT_MODEL = "gemini-2.5-flash"  # fast & cheap

# or
# CHAT_MODEL = "gemini-1.5-pro-001"  # more powerful, if available to you


def get_chat_model(tools=None):
    # tools is a list like [{"function_declarations": [...] }]
    if tools:
        return genai.GenerativeModel(model_name=CHAT_MODEL, tools=tools)
    return genai.GenerativeModel(model_name=CHAT_MODEL)


def embed_text(text: str):
    res = genai.embed_content(model=EMBED_MODEL, content=text)
    return res["embedding"]


def embed_texts(texts):
    res = genai.embed_content(model=EMBED_MODEL, content=texts)
    # If single text, it's dict; if multi, it's list
    if isinstance(res, dict):
        return [res["embedding"]]
    return [r["embedding"] for r in res["embedding"]]
