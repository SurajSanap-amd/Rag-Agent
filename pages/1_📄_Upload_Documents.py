import streamlit as st
import os
import time
from PIL import Image
from src.rag import ingest_file

st.set_page_config(page_title="Upload Documents", page_icon="📄")

st.title("📄 Upload Documents into Vector DB")

# ---------- Hacker-style intro animation (runs once per session) ----------
def run_intro_animation():
    container = st.container()
    with container:
        st.markdown("#### Initializing AI Knowledge Base...")

        terminal = st.empty()
        progress = st.progress(0)

        steps = [
            "Booting AI agent core...",
            "Config ready to Scanning",
            "Config ready to Upload files – PDFs or TXT",
            "Config ready to chunk the content",
            "Config ready to embeddings",
            "Config ready to Store VectorDB ",
            "System ready. Awaiting your documents...",
        ]

        total_time = 5.0  # seconds fake load
        step_time = total_time / len(steps)

        for i, line in enumerate(steps):
            # Hacker-style terminal text
            terminal.markdown(
                f"""```bash
> {line}
```""",
                unsafe_allow_html=True,
            )
            progress.progress((i + 1) / len(steps))
            time.sleep(step_time)

        # Clear progress bar after animation
        progress.empty()


if "intro_shown_upload" not in st.session_state:
    run_intro_animation()
    st.session_state["intro_shown_upload"] = True

st.write("---")

# ---------- Top layout: text + image (static, after animation) ----------
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("What this page does 🧠")
    st.markdown(
        """
        - Turns your **notes** into a searchable knowledge base  
        - Lets the agent answer questions **based on your docs**  
        - Uses **RAG + Gemini embeddings** behind the scenes  
        """
    )

# with col_right:
#     sticker_path = "static/upload_sticker.png"  # Put some cool image here
#     if os.path.exists(sticker_path):
#         sticker = Image.open(sticker_path)
#         sticker = sticker.resize((260, 260))
#         st.image(sticker)
#     else:
#         st.info("Add an image at `static/upload_sticker.png` to show a graphic here.")

st.write("---")

# ---------- Upload card ----------
with st.container():
    st.subheader("Upload your documents 📎")
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files to add into the knowledge base",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="You can upload multiple files at once.",
    )

    ingest_button = st.button("Ingest Files into Vector DB 🚀", use_container_width=True)

# ---------- Ingestion logic with dynamic status text ----------
if ingest_button:
    if not uploaded_files:
        st.warning("Please upload at least one file first.")
    else:
        status_placeholder = st.empty()
        progress_bar = st.progress(0)

        total_chunks = 0
        total_files = len(uploaded_files)

        for index, uf in enumerate(uploaded_files, start=1):
            file_name = uf.name

            status_placeholder.markdown(
                f"```bash\n[{index}/{total_files}] Reading `{file_name}`...\n```"
            )
            bytes_data = uf.read()

            status_placeholder.markdown(
                "```bash\n✂️ Splitting into semantic chunks...\n```"
            )
            chunks_count = ingest_file(bytes_data, file_name)
            total_chunks += chunks_count

            status_placeholder.markdown(
                "```bash\n🧠 Creating embeddings & storing in Vector DB...\n```"
            )

            progress_bar.progress(index / total_files)

        status_placeholder.markdown("```bash\n✅ All files processed successfully.\n```")
        st.success(
            f"Ingested **{total_files}** files. "
            f"Total chunks stored in Vector DB: **{total_chunks}** ✅"
        )

elif not uploaded_files:
    st.info("Upload at least one file to begin.")
