import sqlite3
import json
import os
import numpy as np
from typing import List, Tuple

from .config import VECTOR_DB_PATH
from .gemini_client import embed_text

def _get_conn():
    conn = sqlite3.connect(VECTOR_DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
        """
    )
    return conn

def add_texts(texts: List[str]):
    if not texts:
        return
    conn = _get_conn()
    cur = conn.cursor()
    for t in texts:
        emb = embed_text(t)
        cur.execute(
            "INSERT INTO documents (text, embedding) VALUES (?, ?)",
            (t, json.dumps(emb)),
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

def has_documents() -> bool:
    """Return True if there is at least one document stored in the vector DB."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM documents")
    row = cur.fetchone()
    conn.close()
    count = row[0] if row else 0
    return count > 0
