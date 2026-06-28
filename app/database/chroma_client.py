from pathlib import Path

from app.config import settings


def get_client():
    try:
        import chromadb
        from chromadb.config import Settings
    except ImportError as exc:
        raise ImportError('chromadb is required for vector storage. Install chromadb or mock the client in tests.') from exc

    chrome_dir = Path(settings.chroma_path or 'chroma_db')
    chrome_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.Client(Settings(chroma_db_impl='duckdb+parquet', persist_directory=str(chrome_dir)))
