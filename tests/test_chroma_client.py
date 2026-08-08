import builtins
import sys
import types
from pathlib import Path

import pytest

from app.config import settings
from app.database.chroma_client import get_client


class FakeClient:
    pass


class DummySettings:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_get_client_returns_fake_client(monkeypatch, tmp_path: Path):
    chrome_dir = tmp_path / 'chroma_db'
    settings.chroma_path = str(chrome_dir)

    fake_chromadb = types.ModuleType('chromadb')
    fake_config = types.ModuleType('chromadb.config')
    fake_config.Settings = DummySettings
    fake_chromadb.PersistentClient = lambda path: FakeClient()

    monkeypatch.setitem(sys.modules, 'chromadb', fake_chromadb)
    monkeypatch.setitem(sys.modules, 'chromadb.config', fake_config)

    client = get_client()

    assert isinstance(client, FakeClient)
    assert chrome_dir.exists()


def test_get_client_raises_import_error_when_chromadb_is_missing(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == 'chromadb' or name.startswith('chromadb.'):
            raise ImportError('No module named chromadb')
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, '__import__', fake_import)

    with pytest.raises(ImportError, match='chromadb is required'):  # message from get_client exception chain
        get_client()
