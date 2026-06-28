from pydantic import BaseModel


class ReportResponse(BaseModel):
    context_precision: float
    faithfulness: float
    system_status: str
