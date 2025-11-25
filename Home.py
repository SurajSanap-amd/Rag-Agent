from PIL import Image

import streamlit as st
import json
import os

# Optional: Streamlit Lottie import
try:
    from streamlit_lottie import st_lottie
except Exception:
    def st_lottie(animation, speed=1, loop=True, quality="high", height=None, key=None):
        return None  # fallback

st.set_page_config(page_title="AI Agent RAG Demo", page_icon="🤖", layout="wide")

st.title("🤖 AI Agent with RAG + Tools (Gemini + Streamlit)")


sticker_path = "bot.png"  # 👈 your image path

if os.path.exists(sticker_path):
    sticker = Image.open(sticker_path)
    st.image(sticker, caption=None, width=200)  # change width as needed
else:
    st.warning("⚠️ Sticker not found. Add image at `static/sticker.png`")

# ---------- Lottie Animation ----------
lottie_path = "Robot.json"  # 👈 Make sure your file exists here


if os.path.exists(lottie_path):
    try:
        with open(lottie_path, "r", encoding="utf-8") as anim_source:
            animation = json.load(anim_source)
            st_lottie(
                animation,
                speed=1,
                loop=True,
                quality="high",
                height=200,
                key="robot"
            )
    except Exception as e:
        st.warning(f"⚠️ Could not load animation: {e}")
else:
    st.info("ℹ️ Place Lottie file in `static/AI Lens.json` to show animation here.")

# ---------- Description ----------
st.write(
    """
Welcome! This multi-page app demonstrates:

- **AI Agent** using **Gemini** (function calling)
- **RAG (Retrieval-Augmented Generation)** from your uploaded documents
- **Tools**:
    - `search_documents` (RAG search)
    - `calculate_expression` (calculator)
    - `manage_todos` (todo manager)
- **Vector Store**: simple custom vector DB using **SQLite + embeddings**

📌 Use the pages from the sidebar:
1. **Upload Documents** → store in Vector DB  
2. **Chat with Agent** → ask questions / use tools  
3. **Tools Only Demo** → directly test tools
"""
)

st.info("💡 Tip: First go to **Upload Documents** and add some PDFs or text files.")
