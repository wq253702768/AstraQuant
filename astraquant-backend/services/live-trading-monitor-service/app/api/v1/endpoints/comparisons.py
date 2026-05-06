from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_paper_live_comparison_service import QueryPaperLiveComparisonService
router=APIRouter(prefix="/live-monitor/comparisons", tags=["live-monitor"])
@router.get("/paper-live")
async def query(request: Request): return success_response(await QueryPaperLiveComparisonService().execute(), request)
