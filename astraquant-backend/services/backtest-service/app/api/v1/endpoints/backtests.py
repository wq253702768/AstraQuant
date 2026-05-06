from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.cancel_backtest_task_service import CancelBacktestTaskService
from app.application.services.create_backtest_task_service import CreateBacktestTaskService
from app.application.services.query_backtest_status_service import QueryBacktestStatusService
from app.application.services.query_backtest_summary_service import QueryBacktestSummaryService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.backtest import CreateBacktestRequest

router = APIRouter(prefix="/backtests", tags=["backtests"])

@router.post("")
async def create_backtest(payload: CreateBacktestRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str | None = Depends(get_operator_id)):
    result = await CreateBacktestTaskService(session).execute(payload, operator_id)
    await session.commit()
    return success_response(result, request)

@router.get("/{task_id}/status")
async def status(task_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    return success_response(await QueryBacktestStatusService(session).execute(task_id), request)

@router.get("/{task_id}/summary")
async def summary(task_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    return success_response(await QueryBacktestSummaryService(session).execute(task_id), request)

@router.post("/{task_id}/cancel")
async def cancel(task_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    result = await CancelBacktestTaskService(session).execute(task_id)
    await session.commit()
    return success_response(result, request)
