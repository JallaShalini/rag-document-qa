import pytest
import requests

from app.config import settings
from app.services.llm_service import LLMServiceError, call_llm


def test_call_llm_returns_text_for_valid_response(monkeypatch):
    settings.llm_api_key = 'test-key'

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {'choices': [{'message': {'content': 'Hello from LLM'}}]}

    monkeypatch.setattr('app.services.llm_service.requests.post', lambda *args, **kwargs: FakeResponse())

    assert call_llm('prompt') == 'Hello from LLM'


def test_call_llm_raises_missing_key_error(monkeypatch):
    settings.llm_api_key = None
    monkeypatch.delenv('LLM_API_KEY', raising=False)
    
    result = call_llm('test prompt')
    assert "Based on the uploaded document context" in result


def test_call_llm_raises_timeout_error(monkeypatch):
    settings.llm_api_key = 'test-key'

    def timeout_post(*args, **kwargs):
        raise requests.Timeout()

    monkeypatch.setattr('app.services.llm_service.requests.post', timeout_post)

    with pytest.raises(LLMServiceError, match='LLM request timed out'):
        call_llm('test prompt')


def test_call_llm_raises_authentication_error(monkeypatch):
    settings.llm_api_key = 'test-key'

    class FakeRequestException(requests.RequestException):
        def __init__(self):
            self.response = type('R', (), {'status_code': 401})()

    def auth_post(*args, **kwargs):
        raise FakeRequestException()

    monkeypatch.setattr('app.services.llm_service.requests.post', auth_post)

    with pytest.raises(LLMServiceError, match='LLM authentication failed'):
        call_llm('test prompt')


def test_call_llm_raises_no_choices(monkeypatch):
    settings.llm_api_key = 'test-key'

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {}

    monkeypatch.setattr('app.services.llm_service.requests.post', lambda *args, **kwargs: FakeResponse())

    with pytest.raises(LLMServiceError, match='LLM returned no choices'):
        call_llm('test prompt')
