from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_live_order_service import QueryLiveOrderService
router=APIRouter(prefix="/live-monitor/orders", tags=["live-monitor"])
@router.get("")
async def query(request: Request): return success_response(await QueryLiveOrderService().execute(), request)
