from fastapi import APIRouter, Request

from app.clients.lifecycle_client import LifecycleClient
from app.middleware.permissions import require_permission

router = APIRouter(tags=["lifecycle"])


@router.get("/api/lifecycle/strategies")
async def strategies(request: Request):
    require_permission(request, "lifecycle:read")
    return await LifecycleClient().request("GET", "/lifecycle/strategies", request, params=dict(request.query_params))


@router.get("/api/lifecycle/strategies/{strategy_version_id}")
async def strategy_detail(strategy_version_id: str, request: Request):
    require_permission(request, "lifecycle:read")
    return await LifecycleClient().request("GET", f"/lifecycle/strategies/{strategy_version_id}", request)


@router.get("/api/lifecycle/strategies/{strategy_version_id}/timeline")
async def timeline(strategy_version_id: str, request: Request):
    require_permission(request, "lifecycle:read")
    return await LifecycleClient().request("GET", f"/lifecycle/strategies/{strategy_version_id}/timeline", request)


@router.get("/api/lifecycle/strategies/{strategy_version_id}/evidence")
async def evidence(strategy_version_id: str, request: Request):
    require_permission(request, "lifecycle:read")
    return await LifecycleClient().request("GET", f"/lifecycle/strategies/{strategy_version_id}/evidence", request)


@router.post("/api/lifecycle/strategies/{strategy_version_id}/gates/evaluate")
async def evaluate_gate(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:manage")
    return await LifecycleClient().request("POST", f"/lifecycle/strategies/{strategy_version_id}/gates/evaluate", request, payload)


@router.post("/api/lifecycle/strategies/{strategy_version_id}/applications/small-live")
async def small_live_application(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:apply")
    return await LifecycleClient().request("POST", f"/lifecycle/strategies/{strategy_version_id}/applications/small-live", request, payload)


@router.post("/api/lifecycle/strategies/{strategy_version_id}/applications/scale-up")
async def scale_up_application(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:apply")
    return await LifecycleClient().request("POST", f"/lifecycle/strategies/{strategy_version_id}/applications/scale-up", request, payload)


@router.post("/api/lifecycle/approvals/{approval_id}/approve")
async def approve(approval_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:approve")
    return await LifecycleClient().request("POST", f"/lifecycle/approvals/{approval_id}/approve", request, payload)


@router.post("/api/lifecycle/approvals/{approval_id}/reject")
async def reject(approval_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:approve")
    return await LifecycleClient().request("POST", f"/lifecycle/approvals/{approval_id}/reject", request, payload)


@router.post("/api/lifecycle/strategies/{strategy_version_id}/rollback-to-paper")
async def rollback(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:manage")
    return await LifecycleClient().request("POST", f"/lifecycle/strategies/{strategy_version_id}/rollback-to-paper", request, payload)


@router.post("/api/lifecycle/strategies/{strategy_version_id}/pause")
async def pause(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:manage")
    return await LifecycleClient().request("POST", f"/lifecycle/strategies/{strategy_version_id}/pause", request, payload)


@router.post("/api/lifecycle/strategies/{strategy_version_id}/retire")
async def retire(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "lifecycle:manage")
    return await LifecycleClient().request("POST", f"/lifecycle/strategies/{strategy_version_id}/retire", request, payload)


@router.get("/api/lifecycle/dashboard/overview")
async def dashboard(request: Request):
    require_permission(request, "lifecycle:read")
    return await LifecycleClient().request("GET", "/lifecycle/dashboard/overview", request)
