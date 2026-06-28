import pytest

from app.services.vector_store import VectorStoreError, count_vectors, delete_vectors, insert_vectors, search_vectors


class FakeCollection:
    def __init__(self):
        self.deleted_ids = []
        self.documents = ['a', 'b']
        self.metadatas = [{'id': 1}, {'id': 2}]

    def delete(self, ids):
        self.deleted_ids.extend(ids)

    def count(self):
        return len(self.documents)


def test_delete_vectors_calls_collection_delete(monkeypatch):
    fake_collection = FakeCollection()
    monkeypatch.setattr('app.services.vector_store.get_collection', lambda: fake_collection)

    delete_vectors(['id1', 'id2'])

    assert fake_collection.deleted_ids == ['id1', 'id2']


def test_delete_vectors_raises_vector_store_error(monkeypatch):
    def fail_get_collection():
        raise RuntimeError('collection fail')

    monkeypatch.setattr('app.services.vector_store.get_collection', fail_get_collection)

    with pytest.raises(VectorStoreError, match='Failed to delete vectors'):
        delete_vectors(['id1'])


def test_count_vectors_returns_count(monkeypatch):
    fake_collection = FakeCollection()
    monkeypatch.setattr('app.services.vector_store.get_collection', lambda: fake_collection)

    assert count_vectors() == 2


def test_count_vectors_raises_vector_store_error(monkeypatch):
    def fail_get_collection():
        raise RuntimeError('count fail')

    monkeypatch.setattr('app.services.vector_store.get_collection', fail_get_collection)

    with pytest.raises(VectorStoreError, match='Failed to count vectors'):
        count_vectors()
