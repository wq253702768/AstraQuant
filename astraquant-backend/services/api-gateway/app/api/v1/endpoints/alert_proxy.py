from fastapi import APIRouter, Request
from app.clients.alert_client import AlertClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["alerts"])
@router.get("/api/alerts")
async def alerts(request: Request): require_permission(request,"alert:read"); return await AlertClient().request("GET","/alerts",request,params=dict(request.query_params))
@router.get("/api/alerts/{alert_id}")
async def alert(alert_id: str, request: Request): require_permission(request,"alert:read"); return await AlertClient().request("GET",f"/alerts/{alert_id}",request)
@router.post("/api/alerts/{alert_id}/acknowledge")
async def ack(alert_id: str, payload: dict, request: Request): require_permission(request,"alert:manage"); return await AlertClient().request("POST",f"/alerts/{alert_id}/acknowledge",request,payload)
@router.post("/api/alerts/{alert_id}/resolve")
async def resolve(alert_id: str, payload: dict, request: Request): require_permission(request,"alert:manage"); return await AlertClient().request("POST",f"/alerts/{alert_id}/resolve",request,payload)
@router.post("/api/alerts/suppressions")
async def suppress(payload: dict, request: Request): require_permission(request,"alert:manage"); return await AlertClient().request("POST","/alerts/suppressions",request,payload)
@router.get("/api/alerts/dashboard/overview")
async def dashboard(request: Request): require_permission(request,"alert:read"); return await AlertClient().request("GET","/alerts/dashboard/overview",request)
