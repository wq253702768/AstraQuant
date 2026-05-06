from fastapi import APIRouter, Request
from app.clients.strategy_score_client import StrategyScoreClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["strategy-scores"])
@router.post("/api/strategy-scores/calculate")
async def calculate(payload: dict, request: Request):
    require_permission(request,"strategy:read"); return await StrategyScoreClient().request("POST","/strategy-scores/calculate",request,payload)
@router.get("/api/strategy-scores/{score_id}")
async def get_score(score_id: str, request: Request):
    require_permission(request,"strategy:read"); return await StrategyScoreClient().request("GET",f"/strategy-scores/{score_id}",request)
@router.get("/api/strategy-versions/{strategy_version_id}/score/latest")
async def latest(strategy_version_id: str, request: Request):
    require_permission(request,"strategy:read"); return await StrategyScoreClient().request("GET",f"/strategy-versions/{strategy_version_id}/score/latest",request)
