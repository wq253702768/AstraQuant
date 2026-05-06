from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_drawdowns_service import QueryDrawdownsService

router = APIRouter(prefix="/backtests", tags=["backtests"])

@router.get("/{task_id}/drawdowns")
async def drawdowns(task_id: str, request: Request):
    return success_response(QueryDrawdownsService().execute(task_id), request)
