from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_dashboard_service import QueryDashboardService
router=APIRouter(prefix="/paper-monitor/dashboard", tags=["paper-monitor"])
@router.get("/overview")
async def overview(request: Request): return success_response(await QueryDashboardService().execute(), request)
