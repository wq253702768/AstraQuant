from fastapi import APIRouter, Request
from app.clients.replay_client import ReplayClient
from app.middleware.permissions import require_permission

router = APIRouter(tags=["replays"])

@router.post("/api/replays/build")
async def build(payload: dict, request: Request):
    require_permission(request, "backtest:read")
    return await ReplayClient().request("POST", "/replays/build", request, payload)

@router.get("/api/replays/build/{build_task_id}")
async def build_status(build_task_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await ReplayClient().request("GET", f"/replays/build/{build_task_id}", request)

@router.get("/api/replays/{drawdown_id}/page")
async def page(drawdown_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await ReplayClient().request("GET", f"/replays/{drawdown_id}/page", request)

@router.get("/api/replays/{drawdown_id}/events")
async def events(drawdown_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await ReplayClient().request("GET", f"/replays/{drawdown_id}/events", request, params=dict(request.query_params))

@router.get("/api/replays/{drawdown_id}/klines")
async def klines(drawdown_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await ReplayClient().request("GET", f"/replays/{drawdown_id}/klines", request, params=dict(request.query_params))

@router.get("/api/replays/{drawdown_id}/curves")
async def curves(drawdown_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await ReplayClient().request("GET", f"/replays/{drawdown_id}/curves", request)

@router.get("/api/replays/{drawdown_id}/export")
async def export(drawdown_id: str, request: Request):
    require_permission(request, "backtest:read")
    return await ReplayClient().request("GET", f"/replays/{drawdown_id}/export", request)
