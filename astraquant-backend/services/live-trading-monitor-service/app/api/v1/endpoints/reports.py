from fastapi import APIRouter, Request
from astra_common.response import success_response
router=APIRouter(prefix="/live-monitor/daily-reports", tags=["live-monitor"])
@router.get("")
async def query(request: Request): return success_response({"items": []}, request)
