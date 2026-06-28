import os
import shutil
import tempfile
from pathlib import Path

import os
import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from app.database.chroma_client import get_client
from app.database.collection_manager import delete_collection


try:
    import chromadb  # noqa: F401
    from chromadb.config import Settings  # noqa: F401
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


@pytest.fixture(scope='session', autouse=True)
def configure_test_env():
    original_upload_path = settings.upload_path
    original_chroma_path = settings.chroma_path

    temp_dir = tempfile.mkdtemp(prefix='rag_test_')
    settings.upload_path = os.path.join(temp_dir, 'uploads')
    settings.chroma_path = os.path.join(temp_dir, 'chroma_db')
    os.makedirs(settings.upload_path, exist_ok=True)
    os.makedirs(settings.chroma_path, exist_ok=True)

    if CHROMADB_AVAILABLE:
        settings.chroma_path = settings.chroma_path

    yield

    settings.upload_path = original_upload_path
    settings.chroma_path = original_chroma_path
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(autouse=True)
def clear_vector_store():
    delete_collection()
    yield
    delete_collection()


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def tmp_text_file(tmp_path: Path):
    path = tmp_path / 'sample.txt'
    path.write_text('This is a sample text document for testing.', encoding='utf-8')
    return path


@pytest.fixture()
def tmp_md_file(tmp_path: Path):
    path = tmp_path / 'sample.md'
    path.write_text('# Title\n\nThis is markdown content.', encoding='utf-8')
    return path


@pytest.fixture()
def tmp_pdf_file(tmp_path: Path):
    from reportlab.pdfgen import canvas

    path = tmp_path / 'sample.pdf'
    c = canvas.Canvas(str(path))
    c.drawString(100, 750, 'Hello PDF world')
    c.showPage()
    c.save()
    return path
