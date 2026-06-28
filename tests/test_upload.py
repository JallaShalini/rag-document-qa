import io

from fastapi import status

from app.services.document_processor import extract_text_from_file
from app.services.embedding_service import EmbeddingError
from app.services.vector_store import VectorStoreError


def test_upload_endpoint_rejects_unsupported_file(client):
    data = {'file': ('sample.exe', io.BytesIO(b'test'), 'application/octet-stream')}
    response = client.post('/upload', files=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert body['status_code'] == 400
    assert 'Unsupported file format' in body['error']


def test_upload_endpoint_saves_and_indexes_file(monkeypatch, tmp_text_file, client):
    def fake_embed_texts(chunks):
        return [[0.1] * 10 for _ in chunks]

    def fake_insert_vectors(*args, **kwargs):
        return None

    monkeypatch.setattr('app.api.upload.embed_texts', fake_embed_texts)
    monkeypatch.setattr('app.api.upload.insert_vectors', fake_insert_vectors)

    with tmp_text_file.open('rb') as file_data:
        response = client.post('/upload', files={'file': ('sample.txt', file_data, 'text/plain')})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['message'] == 'File uploaded and indexed successfully.'


def test_extract_text_from_file_parses_txt(tmp_text_file):
    result = extract_text_from_file(str(tmp_text_file))

    assert 'sample text document' in result


def test_upload_endpoint_rejects_empty_extracted_text(monkeypatch, tmp_text_file, client):
    monkeypatch.setattr('app.api.upload.extract_text_from_file', lambda *args, **kwargs: '')
    monkeypatch.setattr('app.api.upload.chunk_text', lambda *args, **kwargs: [])

    with tmp_text_file.open('rb') as file_data:
        response = client.post('/upload', files={'file': ('sample.txt', file_data, 'text/plain')})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert 'extractable text' in body['error']


def test_upload_endpoint_handles_embedding_failure(monkeypatch, tmp_text_file, client):
    monkeypatch.setattr('app.api.upload.embed_texts', lambda *args, **kwargs: (_ for _ in ()).throw(EmbeddingError('embed fail')))
    monkeypatch.setattr('app.api.upload.chunk_text', lambda *args, **kwargs: ['chunk'])
    monkeypatch.setattr('app.api.upload.extract_text_from_file', lambda *args, **kwargs: 'text')

    with tmp_text_file.open('rb') as file_data:
        response = client.post('/upload', files={'file': ('sample.txt', file_data, 'text/plain')})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    body = response.json()
    assert 'Embedding generation failed' in body['error']


def test_upload_endpoint_handles_vector_store_failure(monkeypatch, tmp_text_file, client):
    monkeypatch.setattr('app.api.upload.embed_texts', lambda *args, **kwargs: [[0.1, 0.2, 0.3]])
    monkeypatch.setattr('app.api.upload.insert_vectors', lambda *args, **kwargs: (_ for _ in ()).throw(VectorStoreError('db fail')))
    monkeypatch.setattr('app.api.upload.chunk_text', lambda *args, **kwargs: ['chunk'])
    monkeypatch.setattr('app.api.upload.extract_text_from_file', lambda *args, **kwargs: 'text')

    with tmp_text_file.open('rb') as file_data:
        response = client.post('/upload', files={'file': ('sample.txt', file_data, 'text/plain')})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    body = response.json()
    assert 'Failed to store document vectors' in body['error']


def test_extract_text_from_file_parses_md(tmp_md_file):
    result = extract_text_from_file(str(tmp_md_file))

    assert 'This is markdown content.' in result


def test_extract_text_from_file_parses_pdf(tmp_pdf_file):
    result = extract_text_from_file(str(tmp_pdf_file))

    assert 'Hello PDF world' in result
