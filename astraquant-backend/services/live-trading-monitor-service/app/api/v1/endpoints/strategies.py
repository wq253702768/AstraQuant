from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_live_strategy_service import QueryLiveStrategyService
router=APIRouter(prefix="/live-monitor/strategies", tags=["live-monitor"])
@router.get("/{strategy_version_id}/summary")
async def summary(strategy_version_id: str, request: Request): return success_response(await QueryLiveStrategyService().execute(strategy_version_id), request)
