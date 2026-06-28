from pathlib import Path

from app.utils.helpers import build_metadata, ensure_directory


def test_build_metadata_merges_extra_fields():
    metadata = build_metadata('file.txt', {'chunk_index': 1, 'source': 'test'})

    assert metadata['filename'] == 'file.txt'
    assert metadata['chunk_index'] == 1
    assert metadata['source'] == 'test'


def test_ensure_directory_creates_dir(tmp_path: Path):
    target = tmp_path / 'nested' / 'dir'
    ensure_directory(str(target))

    assert target.exists()
    assert target.is_dir()
