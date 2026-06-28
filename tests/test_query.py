import pytest

from fastapi import status

from app.services.llm_service import LLMServiceError
from app.services.prompt_builder import build_prompt
from app.services.retriever import retrieve_relevant_chunks


def test_query_endpoint_returns_bad_request_for_empty_question(client):
    response = client.post('/query', json={'question': '   '})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert body['status_code'] == 400
    assert 'Question must not be empty' in body['error']


def test_query_endpoint_returns_bad_request_when_no_indices(monkeypatch, client):
    monkeypatch.setattr('app.api.query.retrieve_relevant_chunks', lambda *args, **kwargs: [])

    response = client.post('/query', json={'question': 'What is AI?'})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    body = response.json()
    assert body['status_code'] == 400
    assert 'No indexed documents available' in body['error']


def test_query_endpoint_returns_answer(monkeypatch, client):
    monkeypatch.setattr('app.api.query.retrieve_relevant_chunks', lambda *args, **kwargs: ['ctx'])
    monkeypatch.setattr('app.api.query.build_prompt', lambda *args, **kwargs: 'prompt')
    monkeypatch.setattr('app.api.query.call_llm', lambda prompt: 'answer')

    response = client.post('/query', json={'question': 'What is AI?'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['answer'] == 'answer'
    assert response.json()['sources'] == ['ctx']


def test_query_endpoint_propagates_llm_service_errors(monkeypatch, client):
    def fail_llm(*args, **kwargs):
        raise LLMServiceError('LLM failure')

    monkeypatch.setattr('app.api.query.retrieve_relevant_chunks', lambda *args, **kwargs: ['ctx'])
    monkeypatch.setattr('app.api.query.build_prompt', lambda *args, **kwargs: 'prompt')
    monkeypatch.setattr('app.api.query.call_llm', fail_llm)

    response = client.post('/query', json={'question': 'What is AI?'})

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    body = response.json()
    assert body['status_code'] == 502
    assert 'LLM failure' in body['error']


def test_build_prompt_includes_context_and_question():
    prompt = build_prompt(['doc1', 'doc2'], 'What is the summary?')

    assert 'doc1' in prompt
    assert 'doc2' in prompt
    assert 'What is the summary?' in prompt


def test_retrieve_relevant_chunks_returns_documents(monkeypatch):
    monkeypatch.setattr('app.services.retriever.embed_texts', lambda *args, **kwargs: [[0.1, 0.2, 0.3]])
    monkeypatch.setattr('app.services.retriever.search_vectors', lambda *args, **kwargs: {
        'documents': [['doc one', 'doc two']],
    })

    results = retrieve_relevant_chunks('question')
    assert results == ['doc one', 'doc two']
