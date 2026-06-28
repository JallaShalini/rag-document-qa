from app.constants import CHUNK_OVERLAP
from app.services.chunk_service import chunk_text


def test_chunk_text_returns_empty_when_input_is_empty():
    assert chunk_text('') == []


def test_chunk_text_returns_single_chunk_for_short_text():
    text = 'Hello world'
    assert chunk_text(text) == [text]


def test_chunk_text_creates_overlapping_chunks_for_long_text():
    text = 'x' * 2500
    chunks = chunk_text(text)

    assert len(chunks) == 3
    assert chunks[0][-CHUNK_OVERLAP:] == chunks[1][:CHUNK_OVERLAP]
    assert chunks[1][-CHUNK_OVERLAP:] == chunks[2][:CHUNK_OVERLAP]
