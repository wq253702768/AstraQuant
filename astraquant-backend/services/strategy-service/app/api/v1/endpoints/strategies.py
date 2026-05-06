from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.create_strategy_service import CreateStrategyService
from app.application.services.create_strategy_version_service import CreateStrategyVersionService
from app.application.services.pause_strategy_service import PauseStrategyService
from app.application.services.query_strategy_service import QueryStrategyService
from app.dependencies import get_db_session, get_operator_id
from app.domain.enums.strategy_status import StrategyStatus
from app.schemas.strategy import CreateStrategyRequest, StatusChangeRequest
from app.schemas.strategy_version import CreateStrategyVersionRequest

router = APIRouter(prefix="/strategies", tags=["strategies"])

@router.get("")
async def list_strategies(request: Request, status: str | None = None, strategy_type: str | None = None, keyword: str | None = None, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=200), session: AsyncSession = Depends(get_db_session)):
    result = await QueryStrategyService(session).list_strategies(status, strategy_type, keyword, page, page_size)
    return success_response(result, request)

@router.post("")
async def create_strategy(payload: CreateStrategyRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str = Depends(get_operator_id)):
    result = await CreateStrategyService(session).execute(payload, operator_id, getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)

@router.get("/{strategy_id}")
async def get_strategy(strategy_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    result = await QueryStrategyService(session).get_strategy(strategy_id)
    return success_response(result, request)

@router.post("/{strategy_id}/versions")
async def create_version(strategy_id: str, payload: CreateStrategyVersionRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str = Depends(get_operator_id)):
    result = await CreateStrategyVersionService(session).execute(strategy_id, payload, operator_id, getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)

@router.post("/{strategy_id}/pause")
async def pause(strategy_id: str, payload: StatusChangeRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str = Depends(get_operator_id)):
    result = await PauseStrategyService(session).change_status(strategy_id, StrategyStatus.PAUSED, payload.reason, operator_id, getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)

@router.post("/{strategy_id}/retire")
async def retire(strategy_id: str, payload: StatusChangeRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str = Depends(get_operator_id)):
    result = await PauseStrategyService(session).change_status(strategy_id, StrategyStatus.RETIRED, payload.reason, operator_id, getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)
