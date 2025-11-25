from typing import List

def simple_chunk_text(text: str, max_chars: int = 800) -> List[str]:
    text = " ".join(text.split())
    chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
    return chunks
