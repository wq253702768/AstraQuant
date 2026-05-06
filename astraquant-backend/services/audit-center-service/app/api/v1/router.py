from fastapi import APIRouter, Request
from astra_common.response import success_response
api_router=APIRouter()
@api_router.get("/audit/events")
async def events(request: Request): return success_response({"items": [], "total": 0}, request)
@api_router.get("/audit/events/{event_id}")
async def event(event_id: str, request: Request): return success_response({"audit_event_id": event_id}, request)
@api_router.get("/audit/traces/{trace_id}")
async def trace(trace_id: str, request: Request): return success_response({"trace_id": trace_id, "events": []}, request)
@api_router.post("/audit/exports")
async def export(request: Request): return success_response({"export_task_id":"exp_mock","status":"QUEUED"}, request)
@api_router.get("/audit/dashboard/overview")
async def dashboard(request: Request): return success_response({"today_event_count":0,"critical_event_count":0}, request)
