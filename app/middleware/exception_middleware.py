from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.utils.logger import log_error
from app.utils.response_formatter import format_error_response


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            if response.status_code >= 500:
                log_error(Exception('Server error'), f'HTTP {response.status_code}')
            return response
        except StarletteHTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content=format_error_response(str(exc.detail), exc.status_code),
            )
        except RequestValidationError as exc:
            log_error(exc, 'request_validation_error')
            return JSONResponse(
                status_code=422,
                content=format_error_response('Invalid request payload', 422, detail=str(exc)),
            )
        except Exception as exc:
            log_error(exc, 'Unexpected exception')
            return JSONResponse(
                status_code=500,
                content=format_error_response('Internal server error', 500),
            )
