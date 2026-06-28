from app.models.embedding_model import EmbeddingModel
from app.utils.logger import log_error


class EmbeddingError(Exception):
    pass


def embed_texts(text_chunks: list[str]) -> list[list[float]]:
    try:
        embeddings = EmbeddingModel.encode(text_chunks, convert_to_numpy=True)
        if hasattr(embeddings, 'tolist'):
            return embeddings.tolist()
        return embeddings
    except Exception as exc:
        log_error(exc, 'embed_texts')
        raise EmbeddingError('Failed to generate embeddings') from exc
