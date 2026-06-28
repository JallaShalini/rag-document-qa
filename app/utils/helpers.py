import os
from pathlib import Path
from typing import Any, Dict


def ensure_directory(path: str) -> None:
    directory = Path(path)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)


def build_metadata(filename: str, extra: Dict[str, Any] | None = None) -> Dict[str, Any]:
    data = {'filename': filename}
    if extra:
        data.update(extra)
    return data
