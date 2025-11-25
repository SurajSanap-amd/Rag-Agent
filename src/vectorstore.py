import sqlite3
import json
import os
from typing import List, Tuple, Dict

import numpy as np

from .config import VECTOR_DB_PATH, UPLOAD_DIR
from .gemini_client import embed_text


def _get_conn():
    """Create the SQLite connection and ensure schema exists."""
    os.makedirs(os.path.dirname(VECTOR_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(VECTOR_DB_PATH)
    cur = conn.cursor()
    # Table stores chunks (text + embedding) and the originating file_name
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            embedding TEXT NOT NULL,
            file_name TEXT
        )
        """
    )
    conn.commit()
    return conn


def add_texts(texts: List[str], file_name: str | None = None):
    """Add multiple text chunks to the vector store, tagged with file_name."""
    if not texts:
        return
    conn = _get_conn()
    cur = conn.cursor()
    for t in texts:
        emb = embed_text(t)
        cur.execute(
            "INSERT INTO documents (text, embedding, file_name) VALUES (?, ?, ?)",
            (t, json.dumps(emb), file_name),
        )
    conn.commit()
    conn.close()


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def similarity_search(query: str, k: int = 5) -> List[Tuple[str, float]]:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, text, embedding FROM documents")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return []

    q_emb = np.array(embed_text(query), dtype=float)
    scored = []
    for _id, text, emb_json in rows:
        emb = np.array(json.loads(emb_json), dtype=float)
        score = _cosine_sim(q_emb, emb)
        scored.append((text, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


# ---------- Document-level helpers ----------

def has_documents() -> bool:
    """Return True if there is at least one document stored in the vector DB."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM documents")
    row = cur.fetchone()
    conn.close()
    count = row[0] if row else 0
    return count > 0


def list_documents() -> List[Dict[str, int]]:
    """
    Returns a list of dicts:
    [
      {"file_name": "abc.pdf", "chunks": 42},
      ...
    ]
    """
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT file_name, COUNT(*) as cnt
        FROM documents
        WHERE file_name IS NOT NULL
        GROUP BY file_name
        ORDER BY file_name
        """
    )
    rows = cur.fetchall()
    conn.close()

    docs = []
    for file_name, cnt in rows:
        docs.append({"file_name": file_name, "chunks": cnt})
    return docs


def delete_document(file_name: str):
    """
    Delete all vector chunks for a given file_name
    and remove the original uploaded file if it exists.
    """
    # Delete from vector DB
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM documents WHERE file_name = ?", (file_name,))
    conn.commit()
    conn.close()

    # Delete the raw uploaded file
    file_path = os.path.join(UPLOAD_DIR, file_name)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            # ignore file delete errors silently
            pass
