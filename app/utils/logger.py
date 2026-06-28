import logging
import os
from functools import wraps
from logging.handlers import RotatingFileHandler
from time import perf_counter

from app.config import settings

LOG_FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def _ensure_directory(path: str) -> None:
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def _create_handler(path: str, level: int) -> RotatingFileHandler:
    _ensure_directory(path)
    handler = RotatingFileHandler(path, maxBytes=5_242_880, backupCount=3, encoding='utf-8')
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    return handler


app_log_path = settings.log_path or 'logs/app.log'
error_log_path = os.path.join(os.path.dirname(app_log_path), 'error.log')

logger = logging.getLogger('rag_document_qa')
logger.setLevel(logging.INFO)
if not logger.handlers:
    logger.addHandler(_create_handler(app_log_path, logging.INFO))
    logger.addHandler(_create_handler(error_log_path, logging.ERROR))


def log_startup() -> None:
    logger.info('Application startup complete.')


def log_upload(filename: str) -> None:
    logger.info('File uploaded: %s', filename)


def log_query(question: str) -> None:
    logger.info('Query received: %s', question)


def log_error(error: Exception, context: str | None = None) -> None:
    message = f'Error in {context}' if context else 'Unhandled error'
    logger.error('%s: %s', message, str(error), exc_info=True)


def log_execution_time(name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = perf_counter()
            try:
                return await func(*args, **kwargs)
            finally:
                elapsed = perf_counter() - start
                logger.info('%s executed in %.3f seconds', name, elapsed)

        return wrapper

    return decorator
