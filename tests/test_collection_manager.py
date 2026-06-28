import types

from app.database.collection_manager import COLLECTION_NAME, delete_collection, get_collection


class FakeClient:
    def __init__(self, collections):
        self._collections = collections

    def list_collections(self):
        return self._collections

    def get_collection(self, name):
        return self._collections[0]

    def create_collection(self, name):
        collection = types.SimpleNamespace(name=name)
        self._collections.append(collection)
        return collection

    def delete_collection(self, name):
        self._collections = [c for c in self._collections if c.name != name]


class FakeCollection:
    def __init__(self, name):
        self.name = name


def test_get_collection_returns_existing_collection(monkeypatch):
    existing = FakeCollection(COLLECTION_NAME)
    fake_client = FakeClient([existing])

    monkeypatch.setattr('app.database.collection_manager.get_client', lambda: fake_client)

    collection = get_collection()

    assert collection is existing


def test_get_collection_creates_new_collection_when_missing(monkeypatch):
    fake_client = FakeClient([])
    monkeypatch.setattr('app.database.collection_manager.get_client', lambda: fake_client)

    collection = get_collection()

    assert collection.name == COLLECTION_NAME
    assert any(c.name == COLLECTION_NAME for c in fake_client._collections)


def test_delete_collection_handles_import_error(monkeypatch):
    def raise_import_error():
        raise ImportError('no chromadb')

    monkeypatch.setattr('app.database.collection_manager.get_client', raise_import_error)

    delete_collection()  # should not raise


def test_delete_collection_skips_missing_collection(monkeypatch):
    class Client:
        def list_collections(self):
            return []

    monkeypatch.setattr('app.database.collection_manager.get_client', lambda: Client())

    delete_collection()  # should not raise
