import streamlit as st

from src.vectorstore import list_documents, delete_document

st.set_page_config(page_title="Manage Documents", page_icon="📚")

st.title("📚 Your Uploaded Documents")

st.caption(
    "These are the documents currently stored in the Vector DB. "
    "The AI agent uses them for RAG-based answers."
)

st.write("")

docs = list_documents()

if not docs:
    st.info("No documents uploaded yet. Go to **Upload Documents** page to add some.")
else:
    for doc in docs:
        file_name = doc["file_name"]
        chunks = doc["chunks"]

        with st.container():
            col1, col2, col3 = st.columns([5, 2, 1])

            with col1:
                st.markdown(f"**📄 {file_name}**")
                st.caption(f"Chunks stored in Vector DB: `{chunks}`")

            with col2:
                st.markdown(
                    "<span style='font-size:0.85rem; color:#9ca3af;'>RAG status: ✅ indexed</span>",
                    unsafe_allow_html=True,
                )

            with col3:
                if st.button("Delete", key=f"del_{file_name}"):
                    delete_document(file_name)
                    st.success(f"Deleted `{file_name}` from storage and vector DB.")
                    st.rerun()

        st.write("---")

