from pathlib import Path

from PyPDF2 import PdfReader


def parse_pdf(file_path: str) -> str:
    path = Path(file_path)
    reader = PdfReader(path)
    text_parts = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)

    return '\n'.join(text_parts).strip()
