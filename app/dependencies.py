from fastapi import Depends

from app.config import settings


def get_settings():
    return settings
