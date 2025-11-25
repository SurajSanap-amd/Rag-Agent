import os
from dotenv import load_dotenv

# For local development: reads .env if present
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
VECTOR_DB_PATH = os.path.join(DATA_DIR, "vectordb.sqlite")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_gemini_api_key() -> str:
    """
    Get Gemini API key from (in this order):
    1. Streamlit secrets: GEMINI_API_KEY or GOOGLE_API_KEY  (Streamlit Cloud)
    2. Environment variables: GEMINI_API_KEY or GOOGLE_API_KEY (local dev)
    """

    api_key = ""

    # 1) Try Streamlit secrets (Cloud)
    try:
        import streamlit as st

        # Support both names, in case you used GOOGLE_API_KEY in secrets
        for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
            if key in st.secrets:
                api_key = st.secrets[key]
                break
    except Exception:
        # Not running inside Streamlit yet, skip
        pass

    # 2) Fallback: normal env vars (.env or system)
    if not api_key:
        for key in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
            value = os.getenv(key)
            if value:
                api_key = value
                break

    # 3) If still empty → show nice error in Streamlit, or raise if not in Streamlit
    if not api_key:
        try:
            import streamlit as st

            st.error(
                "🚨 API key for Gemini is not configured.\n\n"
                "Please set **`GEMINI_API_KEY`** or **`GOOGLE_API_KEY`** in Streamlit **Secrets**, "
                "or as an environment variable."
            )
            st.stop()
        except Exception:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY or GOOGLE_API_KEY "
                "in environment or Streamlit secrets."
            )

    return api_key
