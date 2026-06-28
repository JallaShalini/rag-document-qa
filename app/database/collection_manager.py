from app.database.chroma_client import get_client


COLLECTION_NAME = 'documents'


def get_collection():
    client = get_client()
    if COLLECTION_NAME in [col.name for col in client.list_collections()]:
        return client.get_collection(name=COLLECTION_NAME)
    return client.create_collection(name=COLLECTION_NAME)


def delete_collection():
    try:
        client = get_client()
        if COLLECTION_NAME in [col.name for col in client.list_collections()]:
            client.delete_collection(name=COLLECTION_NAME)
    except ImportError:
        return
    except Exception:
        return
