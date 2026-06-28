from app.database.collection_manager import get_collection
from app.utils.logger import log_error


class VectorStoreError(Exception):
    pass


def insert_vectors(ids: list[str], embeddings: list[list[float]], metadatas: list[dict], documents: list[str]) -> None:
    try:
        collection = get_collection()
        collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)
    except Exception as exc:
        log_error(exc, 'insert_vectors')
        raise VectorStoreError('Failed to store vectors') from exc


def search_vectors(query_embedding: list[float], top_k: int):
    try:
        collection = get_collection()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances'],
        )
        return results
    except Exception as exc:
        log_error(exc, 'search_vectors')
        raise VectorStoreError('Vector database search failed') from exc


def delete_vectors(ids: list[str]) -> None:
    try:
        collection = get_collection()
        collection.delete(ids=ids)
    except Exception as exc:
        log_error(exc, 'delete_vectors')
        raise VectorStoreError('Failed to delete vectors') from exc


def count_vectors() -> int:
    try:
        collection = get_collection()
        return collection.count()
    except Exception as exc:
        log_error(exc, 'count_vectors')
        raise VectorStoreError('Failed to count vectors') from exc
