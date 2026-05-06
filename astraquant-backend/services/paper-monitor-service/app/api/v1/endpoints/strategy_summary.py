from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_strategy_summary_service import QueryStrategySummaryService
router=APIRouter(prefix="/paper-monitor/strategies", tags=["paper-monitor"])
@router.get("/{strategy_version_id}/daily-summary")
async def query(strategy_version_id: str, request: Request): return success_response(await QueryStrategySummaryService().execute(strategy_version_id), request)
