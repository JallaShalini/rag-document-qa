from fastapi import HTTPException
from starlette.responses import JSONResponse

from app.utils.response_formatter import format_error_response


def handle_http_exception(exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(str(exc.detail), exc.status_code),
    )


def handle_bad_request(detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content=format_error_response(detail, 400),
    )


def handle_validation_error(detail: str) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=format_error_response(detail, 422),
    )


def handle_internal_error(detail: str = 'Internal server error') -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=format_error_response(detail, 500),
    )
