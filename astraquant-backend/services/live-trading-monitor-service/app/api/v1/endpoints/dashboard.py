from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_live_dashboard_service import QueryLiveDashboardService
router=APIRouter(prefix="/live-monitor/dashboard", tags=["live-monitor"])
@router.get("/overview")
async def overview(request: Request): return success_response(await QueryLiveDashboardService().execute(), request)
