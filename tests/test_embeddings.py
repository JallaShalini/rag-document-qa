import pytest

from app.models.embedding_model import EmbeddingModel
from app.services.embedding_service import EmbeddingError, embed_texts


def test_embed_texts_returns_vector_list(monkeypatch):
    monkeypatch.setattr(EmbeddingModel, 'encode', lambda *args, **kwargs: [[0.1, 0.2, 0.3]])

    embeddings = embed_texts(['Hello world'])

    assert isinstance(embeddings, list)
    assert len(embeddings) == 1
    assert isinstance(embeddings[0], list)
    assert len(embeddings[0]) == 3


def test_embed_texts_raises_embedding_error_when_model_fails(monkeypatch):
    def fail_encode(*args, **kwargs):
        raise RuntimeError('model failure')

    monkeypatch.setattr(EmbeddingModel, 'encode', fail_encode)

    with pytest.raises(EmbeddingError):
        embed_texts(['Hello world'])
