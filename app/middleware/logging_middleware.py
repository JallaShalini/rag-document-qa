import time

from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from app.utils.logger import logger


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        method = request.method
        path = request.url.path
        logger.info('Request started: %s %s', method, path)

        start_time = time.perf_counter()

        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                status_code = message['status']
                elapsed = time.perf_counter() - start_time
                logger.info('Response completed: %s %s %s in %.3f sec', method, path, status_code, elapsed)
            await send(message)

        await self.app(scope, receive, send_wrapper)
