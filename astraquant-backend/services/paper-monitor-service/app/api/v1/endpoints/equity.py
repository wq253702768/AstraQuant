from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_equity_curve_service import QueryEquityCurveService
router=APIRouter(prefix="/paper-monitor/equity-curve", tags=["paper-monitor"])
@router.get("")
async def query(request: Request): return success_response(await QueryEquityCurveService().execute(), request)
