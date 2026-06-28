from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse

from app.config import settings
from app.middleware.exception_middleware import ExceptionMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.response_formatter import format_error_response


def configure_app(app: FastAPI) -> None:
    app.state.settings = settings

    if hasattr(app, 'add_event_handler'):
        app.add_event_handler('startup', on_startup)
    else:
        app.router.on_startup.append(on_startup)

    app.add_middleware(ExceptionMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)


async def on_startup() -> None:
    # Future startup logic can be added here.
    pass


async def http_exception_handler(request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(str(exc.detail), exc.status_code),
    )


async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=format_error_response('Invalid request payload', 422, detail=str(exc)),
    )
