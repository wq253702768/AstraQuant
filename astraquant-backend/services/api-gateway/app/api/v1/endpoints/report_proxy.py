from fastapi import APIRouter, Request
from app.clients.report_client import ReportClient
from app.middleware.permissions import require_permission
router=APIRouter(tags=["reports"])
@router.post("/api/reports/build")
async def build(payload: dict, request: Request):
    require_permission(request,"report:build"); return await ReportClient().request("POST","/reports/build",request,payload)
@router.get("/api/reports/tasks/{report_task_id}")
async def task(report_task_id: str, request: Request):
    require_permission(request,"report:read"); return await ReportClient().request("GET",f"/reports/tasks/{report_task_id}",request)
@router.get("/api/reports/tasks/{report_task_id}/files")
async def files(report_task_id: str, request: Request):
    require_permission(request,"report:read"); return await ReportClient().request("GET",f"/reports/tasks/{report_task_id}/files",request)
