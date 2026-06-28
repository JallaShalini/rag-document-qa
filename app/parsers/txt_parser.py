from pathlib import Path


def parse_txt(file_path: str) -> str:
    path = Path(file_path)
    with path.open('r', encoding='utf-8') as file:
        return file.read()
