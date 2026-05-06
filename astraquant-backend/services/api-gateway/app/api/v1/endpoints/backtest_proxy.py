from fastapi import APIRouter, Request
from app.clients.backtest_client import BacktestClient
from app.middleware.permissions import require_permission

router = APIRouter(tags=["backtests"])

@router.post("/api/backtests")
async def create_backtest(payload: dict, request: Request):
    require_permission(request, "backtest:run")
    return await BacktestClient().request("POST", "/backtests", request, payload)

@router.get("/api/backtests/{task_id}/status")
async def status(task_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await BacktestClient().request("GET", f"/backtests/{task_id}/status", request)

@router.get("/api/backtests/{task_id}/summary")
async def summary(task_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await BacktestClient().request("GET", f"/backtests/{task_id}/summary", request)

@router.get("/api/backtests/{task_id}/trades")
async def trades(task_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await BacktestClient().request("GET", f"/backtests/{task_id}/trades", request, params=dict(request.query_params))

@router.get("/api/backtests/{task_id}/drawdowns")
async def drawdowns(task_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await BacktestClient().request("GET", f"/backtests/{task_id}/drawdowns", request)

@router.post("/api/backtests/{task_id}/cancel")
async def cancel(task_id: str, request: Request):
    require_permission(request, "backtest:run")
    return await BacktestClient().request("POST", f"/backtests/{task_id}/cancel", request)
