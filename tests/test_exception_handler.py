from fastapi import HTTPException

from app.utils.exception_handler import (
    handle_bad_request,
    handle_http_exception,
    handle_internal_error,
    handle_validation_error,
)


def test_handle_http_exception_returns_formatted_json_response():
    exc = HTTPException(status_code=404, detail='not found')
    response = handle_http_exception(exc)

    assert response.status_code == 404
    assert response.body.decode() == '{"error":"not found","status_code":404}'


def test_handle_bad_request_returns_400_response():
    response = handle_bad_request('bad request')

    assert response.status_code == 400
    assert 'bad request' in response.body.decode()


def test_handle_validation_error_returns_422_response():
    response = handle_validation_error('invalid payload')

    assert response.status_code == 422
    assert 'invalid payload' in response.body.decode()


def test_handle_internal_error_returns_500_response():
    response = handle_internal_error()

    assert response.status_code == 500
    assert 'Internal server error' in response.body.decode()
