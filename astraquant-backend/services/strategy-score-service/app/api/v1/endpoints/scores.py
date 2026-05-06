from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.calculate_strategy_score_service import CalculateStrategyScoreService
from app.application.services.query_strategy_score_service import QueryStrategyScoreService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.score import CalculateScoreRequest

router = APIRouter(tags=["strategy-scores"])

@router.post("/strategy-scores/calculate")
async def calculate(payload: CalculateScoreRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str | None = Depends(get_operator_id)):
    result = await CalculateStrategyScoreService(session).execute(payload, operator_id)
    await session.commit()
    return success_response(result, request)

@router.get("/strategy-scores/{score_id}")
async def get_score(score_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    return success_response(await QueryStrategyScoreService(session).get(score_id), request)

@router.get("/strategy-versions/{strategy_version_id}/score/latest")
async def latest(strategy_version_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    return success_response(await QueryStrategyScoreService(session).latest(strategy_version_id), request)
