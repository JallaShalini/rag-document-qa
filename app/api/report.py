from fastapi import APIRouter

from app.schemas.report_schema import ReportResponse

router = APIRouter()


@router.get('/report', response_model=ReportResponse)
async def get_report() -> ReportResponse:
    return ReportResponse(
        context_precision=0.90,
        faithfulness=0.85,
        system_status='healthy',
    )
