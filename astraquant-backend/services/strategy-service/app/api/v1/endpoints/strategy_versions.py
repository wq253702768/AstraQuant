from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.submit_backtest_service import SubmitBacktestService
from app.application.services.update_strategy_params_service import UpdateStrategyParamsService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.backtest_submit import SubmitBacktestRequest
from app.schemas.strategy_version import UpdateStrategyParamsRequest

router = APIRouter(prefix="/strategy-versions", tags=["strategy-versions"])

@router.put("/{strategy_version_id}/params")
async def update_params(strategy_version_id: str, payload: UpdateStrategyParamsRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str = Depends(get_operator_id)):
    result = await UpdateStrategyParamsService(session).execute(strategy_version_id, payload, operator_id, getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)

@router.post("/{strategy_version_id}/submit-backtest")
async def submit_backtest(strategy_version_id: str, payload: SubmitBacktestRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str = Depends(get_operator_id)):
    result = await SubmitBacktestService(session).execute(strategy_version_id, payload, operator_id, getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)
