import os
import uuid
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException, status

from app.config import settings
from app.schemas.upload_schema import UploadResponse
from app.services.document_processor import extract_text_from_file
from app.services.chunk_service import chunk_text
from app.services.embedding_service import EmbeddingError, embed_texts
from app.services.vector_store import VectorStoreError, insert_vectors
from app.utils.file_validator import is_supported_file
from app.utils.helpers import build_metadata
from app.utils.logger import log_upload, log_error

router = APIRouter()


def _generate_ids(count: int, prefix: str = 'chunk') -> list[str]:
    return [f'{prefix}_{uuid.uuid4().hex}' for _ in range(count)]


@router.post('/upload', response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    filename = file.filename
    if not is_supported_file(filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Unsupported file format. Please upload .txt, .md, or .pdf',
        )

    upload_dir = settings.upload_path or 'uploads'
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    destination = Path(upload_dir) / filename

    try:
        contents = await file.read()
        destination.write_bytes(contents)

        raw_text = extract_text_from_file(str(destination))
        chunks = chunk_text(raw_text)
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Uploaded document does not contain extractable text.',
            )

        embeddings = embed_texts(chunks)
        ids = _generate_ids(len(chunks))
        metadatas = [build_metadata(filename, {'chunk_index': idx}) for idx in range(len(chunks))]

        insert_vectors(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=chunks)
        log_upload(filename)
        return UploadResponse(message='File uploaded and indexed successfully.')
    except HTTPException:
        raise
    except EmbeddingError as exc:
        log_error(exc, 'upload_file')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Embedding generation failed.',
        )
    except VectorStoreError as exc:
        log_error(exc, 'upload_file')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to store document vectors.',
        )
    except Exception as exc:
        log_error(exc, 'upload_file')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to process uploaded file.',
        )
