from fastapi import APIRouter, Request
from app.clients.live_risk_client import LiveRiskClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["live-risk"])
@router.get("/api/live-risk/states")
async def states(request: Request): require_permission(request,"live_risk:read"); return await LiveRiskClient().request("GET","/live-risk/states",request,params=dict(request.query_params))
@router.get("/api/live-risk/circuit-breakers")
async def breakers(request: Request): require_permission(request,"live_risk:read"); return await LiveRiskClient().request("GET","/live-risk/circuit-breakers",request,params=dict(request.query_params))
@router.get("/api/live-risk/circuit-breakers/{breaker_id}")
async def breaker(breaker_id: str, request: Request): require_permission(request,"live_risk:read"); return await LiveRiskClient().request("GET",f"/live-risk/circuit-breakers/{breaker_id}",request)
@router.post("/api/live-risk/emergency-controls/trigger")
async def trigger(payload: dict, request: Request): require_permission(request,"live_risk:emergency"); return await LiveRiskClient().request("POST","/live-risk/emergency-controls/trigger",request,payload)
@router.post("/api/live-risk/emergency-controls/{control_id}/release")
async def release(control_id: str, payload: dict, request: Request): require_permission(request,"live_risk:emergency"); return await LiveRiskClient().request("POST",f"/live-risk/emergency-controls/{control_id}/release",request,payload)
@router.get("/api/live-risk/rules")
async def rules(request: Request): require_permission(request,"live_risk:read"); return await LiveRiskClient().request("GET","/live-risk/rules",request)
