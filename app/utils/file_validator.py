import os

from app.constants import SUPPORTED_FILE_EXTENSIONS


def is_supported_file(filename: str) -> bool:
    _, ext = os.path.splitext(filename.lower())
    return ext in SUPPORTED_FILE_EXTENSIONS
