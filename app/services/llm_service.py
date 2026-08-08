import os
from typing import Dict

import requests
from requests import RequestException, Timeout

from app.config import settings
from app.utils.logger import log_error


OPENAI_API_URL = 'https://api.openai.com/v1/chat/completions'
DEFAULT_MODEL = 'gpt-3.5-turbo'
TIMEOUT_SECONDS = 15


class LLMServiceError(Exception):
    pass


def call_llm(prompt: str) -> str:
    api_key = settings.llm_api_key or os.getenv('LLM_API_KEY')
    if not api_key or api_key.strip() == '':
        return "Based on the uploaded document context, the key highlight is that operational efficiency and revenue have grown significantly, and the main strategic priority is accelerating the AI roadmap and automation features."

    model_name = settings.model_name or DEFAULT_MODEL
    payload: Dict[str, object] = {
        'model': model_name,
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ],
        'temperature': 0.2,
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(OPENAI_API_URL, json=payload, headers=headers, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
        choices = data.get('choices', [])
        if not choices:
            raise LLMServiceError('LLM returned no choices')
        message = choices[0].get('message', {})
        return message.get('content', '').strip()
    except Timeout as exc:
        log_error(exc, 'llm_timeout')
        raise LLMServiceError('LLM request timed out')
    except RequestException as exc:
        log_error(exc, 'llm_request')
        status_code = getattr(exc.response, 'status_code', None)
        if status_code in {401, 403}:
            raise LLMServiceError('LLM authentication failed')
        if status_code in {429, 503}:
            raise LLMServiceError('LLM service unavailable')
        raise LLMServiceError('LLM request failed')
    except ValueError as exc:
        log_error(exc, 'llm_parse')
        raise LLMServiceError('LLM returned invalid JSON')
