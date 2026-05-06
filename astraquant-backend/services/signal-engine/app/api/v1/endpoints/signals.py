from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.generate_signal_service import GenerateSignalService
from app.application.services.query_signal_service import QuerySignalService
from app.dependencies import get_db_session
from app.schemas.signal import GenerateSignalRequest
router=APIRouter(prefix="/signals", tags=["signals"])
@router.post("/generate")
async def generate(payload: GenerateSignalRequest, request: Request, session: AsyncSession=Depends(get_db_session)):
    result=await GenerateSignalService(session).execute(payload); await session.commit(); return success_response(result, request)
@router.get("")
async def list_signals(request: Request, page:int=Query(1,ge=1), page_size:int=Query(20,ge=1,le=200), session: AsyncSession=Depends(get_db_session)):
    return success_response(await QuerySignalService(session).list(page,page_size), request)
@router.get("/{signal_id}")
async def get_signal(signal_id: str, request: Request, session: AsyncSession=Depends(get_db_session)):
    return success_response(await QuerySignalService(session).get(signal_id), request)
