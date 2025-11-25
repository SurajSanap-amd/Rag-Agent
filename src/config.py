import os
from dotenv import load_dotenv

load_dotenv()

import os
from dotenv import load_dotenv

load_dotenv()  # Local only

def get_gemini_api_key() -> str:
    """
    Read Gemini key from:
    1. Streamlit secrets (for deployment)
    2. .env / environment variable (for local)
    """
    api_key = ""

    # 1) Try Streamlit secrets first
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        pass

    # 2) Fallback to local env
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY", "")

    # 3) Fail gracefully
    if not api_key:
        try:
            import streamlit as st
            st.error("🚨 GEMINI_API_KEY not configured!")
            st.stop()
        except:
            raise ValueError("GEMINI_API_KEY not found in env or st.secrets!")

    return api_key


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
VECTOR_DB_PATH = os.path.join(DATA_DIR, "vectordb.sqlite")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
