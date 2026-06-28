from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app


def test_exception_middleware_returns_json_response():
    client = TestClient(app)

    @app.get('/test-error')
    async def test_error():
        raise HTTPException(status_code=418, detail='I am a teapot')

    response = client.get('/test-error')

    assert response.status_code == 418
    assert response.json()['error'] == 'I am a teapot'
    assert response.json()['status_code'] == 418


def test_exception_middleware_handles_unhandled_exception():
    client = TestClient(app)

    @app.get('/test-unhandled')
    async def test_unhandled():
        raise ValueError('boom')

    response = client.get('/test-unhandled')

    assert response.status_code == 500
    assert response.json()['error'] == 'Internal server error'
