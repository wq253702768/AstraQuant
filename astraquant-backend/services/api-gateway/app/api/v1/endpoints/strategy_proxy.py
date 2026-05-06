from fastapi import APIRouter, Request

from app.clients.strategy_client import StrategyClient
from app.middleware.permissions import require_permission

router = APIRouter(tags=["strategy"])


@router.get("/api/strategy-templates")
async def list_templates(request: Request):
    require_permission(request, "strategy:read")
    return await StrategyClient().request("GET", "/strategy-templates", request)


@router.get("/api/strategy-templates/{template_id}")
async def get_template(template_id: str, request: Request):
    require_permission(request, "strategy:read")
    return await StrategyClient().request("GET", f"/strategy-templates/{template_id}", request)


@router.get("/api/strategies")
async def list_strategies(request: Request):
    require_permission(request, "strategy:read")
    return await StrategyClient().request("GET", "/strategies", request, params=dict(request.query_params))


@router.post("/api/strategies")
async def create_strategy(payload: dict, request: Request):
    require_permission(request, "strategy:create")
    return await StrategyClient().request("POST", "/strategies", request, payload)


@router.get("/api/strategies/{strategy_id}")
async def get_strategy(strategy_id: str, request: Request):
    require_permission(request, "strategy:read")
    return await StrategyClient().request("GET", f"/strategies/{strategy_id}", request)


@router.post("/api/strategies/{strategy_id}/versions")
async def create_version(strategy_id: str, payload: dict, request: Request):
    require_permission(request, "strategy:update")
    return await StrategyClient().request("POST", f"/strategies/{strategy_id}/versions", request, payload)


@router.post("/api/strategies/{strategy_id}/pause")
async def pause_strategy(strategy_id: str, payload: dict, request: Request):
    require_permission(request, "strategy:update")
    return await StrategyClient().request("POST", f"/strategies/{strategy_id}/pause", request, payload)


@router.post("/api/strategies/{strategy_id}/retire")
async def retire_strategy(strategy_id: str, payload: dict, request: Request):
    require_permission(request, "strategy:delete")
    return await StrategyClient().request("POST", f"/strategies/{strategy_id}/retire", request, payload)


@router.put("/api/strategy-versions/{strategy_version_id}/params")
async def update_params(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "strategy:update")
    return await StrategyClient().request(
        "PUT",
        f"/strategy-versions/{strategy_version_id}/params",
        request,
        payload,
    )


@router.post("/api/strategy-versions/{strategy_version_id}/submit-backtest")
async def submit_backtest(strategy_version_id: str, payload: dict, request: Request):
    require_permission(request, "backtest:run")
    return await StrategyClient().request(
        "POST",
        f"/strategy-versions/{strategy_version_id}/submit-backtest",
        request,
        payload,
    )
