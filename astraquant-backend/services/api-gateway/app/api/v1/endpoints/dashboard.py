from fastapi import APIRouter, Request
from astra_common.response import success_response

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/overview")
async def overview(request: Request):
    return success_response({"strategy_count": 0, "running_strategy_count": 0, "backtest_task_count": 0, "system_status": "INITIALIZED"}, request)
