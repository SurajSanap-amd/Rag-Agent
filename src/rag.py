from typing import List
import os
from pypdf import PdfReader

from .config import UPLOAD_DIR
from utils.text_splitter import simple_chunk_text
from .vectorstore import add_texts, similarity_search


def _extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return "\n".join(texts)


def _extract_text_from_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def ingest_file(file_data, filename: str) -> int:
    """Save file, extract text, chunk, embed+store. Returns chunks count."""
    # Save file
    save_path = os.path.join(UPLOAD_DIR, filename)
    with open(save_path, "wb") as f:
        f.write(file_data)

    ext = filename.lower().split(".")[-1]
    if ext == "pdf":
        text = _extract_text_from_pdf(save_path)
    else:
        # treat as plain text
        text = _extract_text_from_txt(save_path)

    chunks = simple_chunk_text(text)
    add_texts(chunks)
    return len(chunks)


def rag_query(question: str, k: int = 5) -> str:
    matches = similarity_search(question, k=k)
    if not matches:
        return "No documents found in the vector store yet."
    lines = []
    for i, (txt, score) in enumerate(matches, start=1):
        lines.append(f"[{i}] (score={score:.3f}) {txt}")
    return "\n\n---\n\n".join(lines)
