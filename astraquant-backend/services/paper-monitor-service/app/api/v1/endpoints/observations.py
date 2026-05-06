from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.errors import AppError
from astra_common.response import success_response
from app.application.services.create_observation_service import CreateObservationService
from app.dependencies import get_db_session, get_operator_id
from app.infrastructure.repositories.observation_repository import ObservationRepository
from app.schemas.observation import CreateObservationRequest
router=APIRouter(prefix="/paper-monitor/observations", tags=["paper-monitor"])
@router.post("")
async def create(payload: CreateObservationRequest, request: Request, session: AsyncSession=Depends(get_db_session), operator_id: str|None=Depends(get_operator_id)):
    result=await CreateObservationService(session).execute(payload, operator_id); await session.commit(); return success_response(result, request)
@router.get("/{observation_id}")
async def get(observation_id: str, request: Request, session: AsyncSession=Depends(get_db_session)):
    obs=await ObservationRepository(session).get(observation_id)
    if not obs: raise AppError("OBSERVATION_NOT_FOUND","观察周期不存在",404)
    return success_response({"observation_id":obs.id,"account_id":obs.account_id,"strategy_id":obs.strategy_id,"strategy_version_id":obs.strategy_version_id,"exchange":obs.exchange,"symbols":obs.symbols,"start_time":obs.start_time,"end_time":obs.end_time,"min_observation_days":obs.min_observation_days,"status":obs.status,"latest_admission_result_id":obs.latest_admission_result_id}, request)
