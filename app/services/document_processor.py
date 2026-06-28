import os
from pathlib import Path

from fastapi import HTTPException, status

from app.parsers.txt_parser import parse_txt
from app.parsers.md_parser import parse_md
from app.parsers.pdf_parser import parse_pdf
from app.utils.file_validator import is_supported_file


def extract_text_from_file(file_path: str) -> str:
    filename = os.path.basename(file_path)
    if not is_supported_file(filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Unsupported file format. Please upload .txt, .md, or .pdf',
        )

    extension = Path(filename).suffix.lower()
    if extension == '.txt':
        return parse_txt(file_path)
    if extension == '.md':
        return parse_md(file_path)
    if extension == '.pdf':
        text = parse_pdf(file_path)
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='PDF contains no readable text.',
            )
        return text

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Unsupported file format. Please upload .txt, .md, or .pdf',
    )
