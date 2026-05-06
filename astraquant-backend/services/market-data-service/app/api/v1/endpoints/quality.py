from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.errors import AppError
from astra_common.response import success_response
from app.application.services.query_quality_report_service import QueryQualityReportService
from app.dependencies import get_db_session
from app.schemas.quality import QualityReportResponse

router = APIRouter(prefix="/market-data/quality", tags=["market-data"])

@router.get("")
async def get_quality(request: Request, exchange: str, symbol: str, data_type: str, timeframe: str | None = None, session: AsyncSession = Depends(get_db_session)):
    report = await QueryQualityReportService(session).latest(exchange, symbol, data_type, timeframe)
    if not report:
        raise AppError("DATA_QUALITY_REPORT_NOT_FOUND", "数据质量报告不存在", 404)
    return success_response(QualityReportResponse(status=report.status, expected_count=report.expected_count, actual_count=report.actual_count, missing_count=report.missing_count, duplicate_count=report.duplicate_count, abnormal_count=report.abnormal_count, missing_ranges=report.missing_ranges, warning_items=report.warning_items), request)
