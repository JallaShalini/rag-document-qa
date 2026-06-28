from typing import List

from app.constants import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str) -> List[str]:
    if not text:
        return []

    chunks: List[str] = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        if end >= text_length:
            break
        start = end - CHUNK_OVERLAP

    return chunks
