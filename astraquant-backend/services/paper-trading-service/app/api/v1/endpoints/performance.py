from fastapi import APIRouter, Request
from astra_common.response import success_response
router=APIRouter(prefix="/paper-trading/performance", tags=["paper-trading"])
@router.get("/strategies/{strategy_version_id}")
async def perf(strategy_version_id: str, request: Request): return success_response({"strategy_version_id": strategy_version_id, "total_return": "0", "trade_count": 0}, request)
