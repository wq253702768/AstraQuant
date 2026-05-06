from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_live_position_service import QueryLivePositionService
router=APIRouter(prefix="/live-monitor/positions", tags=["live-monitor"])
@router.get("")
async def query(request: Request): return success_response(await QueryLivePositionService().execute(), request)
