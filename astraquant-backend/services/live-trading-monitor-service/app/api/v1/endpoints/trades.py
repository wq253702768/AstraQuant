from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_live_trade_service import QueryLiveTradeService
router=APIRouter(prefix="/live-monitor/trades", tags=["live-monitor"])
@router.get("")
async def query(request: Request): return success_response(await QueryLiveTradeService().execute(), request)
