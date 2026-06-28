from typing import List

from app.constants import TOP_K
from app.services.embedding_service import embed_texts
from app.services.vector_store import search_vectors


def retrieve_relevant_chunks(question: str, top_k: int = TOP_K) -> List[str]:
    question_embedding = embed_texts([question])[0]
    search_results = search_vectors(question_embedding, top_k)

    documents = search_results.get('documents', [])
    if documents and isinstance(documents[0], list):
        return documents[0]
    return []
