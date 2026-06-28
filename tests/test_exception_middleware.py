import json

import pytest
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.types import Scope

from app.middleware.exception_middleware import ExceptionMiddleware
from app.utils.response_formatter import format_error_response


async def dummy_receive() -> dict:
    return {'type': 'http.request'}


class FakeResponse:
    def __init__(self, status_code=200):
        self.status_code = status_code


def make_request():
    scope: Scope = {'type': 'http', 'method': 'GET', 'path': '/', 'headers': [], 'query_string': b''}
    return Request(scope, receive=dummy_receive)


@pytest.mark.asyncio
async def test_dispatch_returns_response_for_normal_request():
    async def fake_next(request):
        return FakeResponse(status_code=200)

    middleware = ExceptionMiddleware(fake_next)
    response = await middleware.dispatch(make_request(), fake_next)

    assert isinstance(response, FakeResponse)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dispatch_handles_starlette_http_exception():
    async def raise_http_exception(request):
        raise StarletteHTTPException(status_code=404, detail='not found')

    middleware = ExceptionMiddleware(None)
    response = await middleware.dispatch(make_request(), raise_http_exception)

    assert response.status_code == 404
    assert json.loads(response.body.decode()) == format_error_response('not found', 404)


@pytest.mark.asyncio
async def test_dispatch_handles_request_validation_error():
    async def raise_validation_error(request):
        raise RequestValidationError([{'loc': ('body', 'question'), 'msg': 'field required', 'type': 'value_error.missing'}])

    middleware = ExceptionMiddleware(None)
    response = await middleware.dispatch(make_request(), raise_validation_error)

    assert response.status_code == 422
    body = json.loads(response.body.decode())
    assert body['error'] == 'Invalid request payload'
    assert body['status_code'] == 422
    assert 'field required' in body['detail']


@pytest.mark.asyncio
async def test_dispatch_handles_unexpected_exception():
    async def raise_generic_error(request):
        raise RuntimeError('boom')

    middleware = ExceptionMiddleware(None)
    response = await middleware.dispatch(make_request(), raise_generic_error)

    assert response.status_code == 500
    assert json.loads(response.body.decode()) == format_error_response('Internal server error', 500)
