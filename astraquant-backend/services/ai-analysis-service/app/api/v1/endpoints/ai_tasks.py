from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.create_ai_task_service import CreateAITaskService
from app.application.services.query_ai_task_service import QueryAITaskService
from app.dependencies import get_db_session, get_operator_id
from app.schemas.ai_task import CreateAIBacktestAnalysisRequest

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/backtest-analysis")
async def create(payload: CreateAIBacktestAnalysisRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str | None = Depends(get_operator_id)):
    result = await CreateAITaskService(session).execute(payload, operator_id, getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)

@router.get("/tasks/{ai_task_id}/status")
async def status(ai_task_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    return success_response(await QueryAITaskService(session).status(ai_task_id), request)
