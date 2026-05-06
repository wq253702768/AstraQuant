from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.create_live_observation_service import CreateLiveObservationService
from app.application.services.calculate_live_admission_service import CalculateLiveAdmissionService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.observation import CreateLiveObservationRequest
router=APIRouter(prefix="/live-monitor/observations", tags=["live-monitor"])
@router.post("")
async def create(payload: CreateLiveObservationRequest, request: Request, session: AsyncSession=Depends(get_db_session), operator_id: str|None=Depends(get_operator_id)):
    result=await CreateLiveObservationService(session).execute(payload, operator_id); await session.commit(); return success_response(result, request)
@router.post("/{observation_id}/admission/calculate")
async def calculate(observation_id: str, request: Request, session: AsyncSession=Depends(get_db_session)):
    result=await CalculateLiveAdmissionService(session).execute(observation_id); await session.commit(); return success_response(result, request)
