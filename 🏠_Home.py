from PIL import Image

import streamlit as st
import json
import os
# Lottie animation support (with fallback)
try:
    from streamlit_lottie import st_lottie
except Exception:
    def st_lottie(*args, **kwargs):
        # fallback if package missing
        return None


# Optional: Streamlit Lottie import


st.set_page_config(page_title="AI Agent RAG Demo", page_icon="🤖", layout="wide")

st.title("🤖 AI Agent with RAG + Tools (Gemini + Streamlit)")


# sticker_path = "bot.png"  # 👈 your image path

# if os.path.exists(sticker_path):
#     sticker = Image.open(sticker_path)
#     st.image(sticker, caption=None, width=200)  # change width as needed
# else:
#     st.warning("⚠️ Sticker not found. Add image at `static/sticker.png`")

# ---------- Lottie Animation ----------
lottie_path = 'Robot.json'  # 👈 Make sure your file exists here


if os.path.exists(lottie_path):
    try:
        with open(lottie_path, "r", encoding="utf-8") as anim_source:
            animation_data = json.load(anim_source)

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st_lottie(
                animation_data,
                speed=1,
                loop=True,
                quality="high",
                height=350,
                key="lottie-ai-lens"
            )


    except UnicodeDecodeError as e:
        st.error(f"⚠️ Error decoding the animation file: {e}")
    except json.JSONDecodeError as e:
        st.error(f"⚠️ Invalid JSON format: {e}")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")

else:
    st.info("ℹ️ Place Lottie file at `Robot.json` to show animation here.")

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


# ---------- Footer ----------
st.markdown(
    """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background: rgba(0, 0, 0, 0.65);
            text-align: center;
            padding: 10px 0;
            color: white;
            font-size: 14px;
            font-family: 'Segoe UI', sans-serif;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .footer-text {
            background: linear-gradient(90deg, #00eaff, #6e00ff);
            -webkit-background-clip: text;
            color: transparent;
            font-weight: 600;
        }
    </style>

    <div class="footer">
        <span class="footer-text">🚀 Built by Suraj Sanap</span>
    </div>
    """,
    unsafe_allow_html=True,
)
