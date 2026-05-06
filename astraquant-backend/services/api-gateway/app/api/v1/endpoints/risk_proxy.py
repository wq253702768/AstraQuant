from fastapi import APIRouter, Request
from app.clients.risk_client import RiskClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["risk"])
@router.get("/api/risk/decisions")
async def decisions(request: Request): require_permission(request,"risk:read"); return await RiskClient().request("GET","/risk/decisions",request,params=dict(request.query_params))
@router.get("/api/risk/decisions/{decision_id}")
async def decision(decision_id: str, request: Request): require_permission(request,"risk:read"); return await RiskClient().request("GET",f"/risk/decisions/{decision_id}",request)
@router.get("/api/risk/rules")
async def rules(request: Request): require_permission(request,"risk:read"); return await RiskClient().request("GET","/risk/rules",request)
@router.post("/api/risk/check")
async def check(payload: dict, request: Request): require_permission(request,"risk:manage"); return await RiskClient().request("POST","/risk/check",request,payload)
