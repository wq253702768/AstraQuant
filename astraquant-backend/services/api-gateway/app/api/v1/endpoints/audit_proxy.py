from fastapi import APIRouter, Request
from app.clients.audit_client import AuditClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["audit"])
@router.get("/api/audit/events")
async def events(request: Request): require_permission(request,"audit:read"); return await AuditClient().request("GET","/audit/events",request,params=dict(request.query_params))
@router.get("/api/audit/events/{event_id}")
async def event(event_id: str, request: Request): require_permission(request,"audit:read"); return await AuditClient().request("GET",f"/audit/events/{event_id}",request)
@router.get("/api/audit/traces/{trace_id}")
async def trace(trace_id: str, request: Request): require_permission(request,"audit:read"); return await AuditClient().request("GET",f"/audit/traces/{trace_id}",request)
@router.post("/api/audit/exports")
async def export(payload: dict, request: Request): require_permission(request,"audit:export"); return await AuditClient().request("POST","/audit/exports",request,payload)
@router.get("/api/audit/dashboard/overview")
async def dashboard(request: Request): require_permission(request,"audit:read"); return await AuditClient().request("GET","/audit/dashboard/overview",request)
