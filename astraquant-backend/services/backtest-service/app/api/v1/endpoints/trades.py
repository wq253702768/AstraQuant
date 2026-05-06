from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_backtest_trades_service import QueryBacktestTradesService

router = APIRouter(prefix="/backtests", tags=["backtests"])

@router.get("/{task_id}/trades")
async def trades(task_id: str, request: Request):
    return success_response(QueryBacktestTradesService().execute(task_id), request)
