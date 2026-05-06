from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.calculate_admission_service import CalculateAdmissionService
from app.application.services.query_admission_result_service import QueryAdmissionResultService
from app.dependencies import get_db_session
router=APIRouter(prefix="/paper-monitor", tags=["paper-monitor"])
@router.post("/observations/{observation_id}/admission/calculate")
async def calculate(observation_id: str, request: Request, session: AsyncSession=Depends(get_db_session)):
    result=await CalculateAdmissionService(session).execute(observation_id); await session.commit(); return success_response(result, request)
@router.get("/admission-results/{result_id}")
async def result(result_id: str, request: Request, session: AsyncSession=Depends(get_db_session)):
    return success_response(await QueryAdmissionResultService(session).execute(result_id), request)
