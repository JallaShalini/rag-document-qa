import pytest

from app.services.vector_store import VectorStoreError, count_vectors, insert_vectors, search_vectors


class FakeCollection:
    def __init__(self):
        self._documents = []
        self._metadatas = []

    def add(self, ids, embeddings, metadatas, documents):
        self._documents.extend(documents)
        self._metadatas.extend(metadatas)

    def query(self, query_embeddings, n_results, include):
        return {
            'documents': [self._documents[:n_results]],
            'metadatas': [self._metadatas[:n_results]],
            'distances': [[0.0 for _ in range(min(n_results, len(self._documents)))]]
        }

    def count(self):
        return len(self._documents)


def test_vector_store_insert_and_search_round_trip(monkeypatch):
    fake_collection = FakeCollection()
    monkeypatch.setattr('app.services.vector_store.get_collection', lambda: fake_collection)

    insert_vectors(
        ids=['chunk1'],
        embeddings=[[0.1, 0.2, 0.3]],
        metadatas=[{'source': 'test'}],
        documents=['test document'],
    )

    assert count_vectors() == 1

    results = search_vectors([0.1, 0.2, 0.3], top_k=1)
    assert results['documents'][0][0] == 'test document'
    assert results['metadatas'][0][0]['source'] == 'test'


def test_vector_store_insert_raises_when_collection_fails(monkeypatch):
    import app.services.vector_store as vs

    def fail_get_collection():
        raise RuntimeError('collection failure')

    monkeypatch.setattr(vs, 'get_collection', fail_get_collection)

    with pytest.raises(VectorStoreError, match='Failed to store vectors'):
        insert_vectors(ids=['chunk1'], embeddings=[[0.1]], metadatas=[{}], documents=['text'])
