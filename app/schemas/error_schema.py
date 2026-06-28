from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    error: str
    status_code: int
    detail: Optional[str] = None
