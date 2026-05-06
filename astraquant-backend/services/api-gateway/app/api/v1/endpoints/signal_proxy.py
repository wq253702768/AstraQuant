from fastapi import APIRouter, Request
from app.clients.signal_client import SignalClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["signals"])
@router.get("/api/signals")
async def list_signals(request: Request): require_permission(request,"signal:read"); return await SignalClient().request("GET","/signals",request,params=dict(request.query_params))
@router.get("/api/signals/{signal_id}")
async def get_signal(signal_id: str, request: Request): require_permission(request,"signal:read"); return await SignalClient().request("GET",f"/signals/{signal_id}",request)
@router.get("/api/signal-runtime/strategies")
async def runtime_strategies(request: Request): require_permission(request,"signal:read"); return await SignalClient().request("GET","/signal-runtime/strategies",request)
@router.post("/api/signal-runtime/reload")
async def reload(request: Request): require_permission(request,"signal:manage"); return await SignalClient().request("POST","/signal-runtime/reload",request)
@router.post("/api/signal-runtime/strategies/{strategy_version_id}/pause")
async def pause(strategy_version_id: str, payload: dict, request: Request): require_permission(request,"signal:manage"); return await SignalClient().request("POST",f"/signal-runtime/strategies/{strategy_version_id}/pause",request,payload)
