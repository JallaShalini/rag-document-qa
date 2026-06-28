import time
import asyncio

import pytest

from app.utils import logger as app_logger


def test_ensure_directory_creates_nested_dirs(tmp_path):
    target = tmp_path / 'logs' / 'app.log'
    app_logger._ensure_directory(str(target))

    assert target.parent.exists()
    assert target.parent.is_dir()


def test_log_startup_and_query_calls_logger(monkeypatch):
    called = []

    def fake_info(msg, *args, **kwargs):
        called.append(msg)

    monkeypatch.setattr(app_logger.logger, 'info', fake_info)

    app_logger.log_startup()
    app_logger.log_query('test')

    assert 'Application startup complete.' in called
    assert any('Query received:' in msg for msg in called)


def test_log_upload_calls_logger(monkeypatch):
    called = []

    def fake_info(msg, *args, **kwargs):
        called.append(msg)

    monkeypatch.setattr(app_logger.logger, 'info', fake_info)

    app_logger.log_upload('file.txt')

    assert any('File uploaded:' in msg for msg in called)


def test_log_error_calls_logger(monkeypatch):
    called = []

    def fake_error(msg, *args, **kwargs):
        called.append((msg, args))

    monkeypatch.setattr(app_logger.logger, 'error', fake_error)

    app_logger.log_error(ValueError('boom'), 'test_context')

    assert any('Error in test_context' in args[0] for _, args in called)


def test_log_execution_time_decorator(monkeypatch):
    called = []

    def fake_info(msg, *args, **kwargs):
        called.append((msg, args))

    monkeypatch.setattr(app_logger.logger, 'info', fake_info)

    @app_logger.log_execution_time('test_func')
    async def test_func():
        time.sleep(0.01)
        return 'ok'

    result = asyncio.run(test_func())

    assert result == 'ok'
    assert any(
        msg == '%s executed in %.3f seconds' and args[0] == 'test_func'
        for msg, args in called
    )
