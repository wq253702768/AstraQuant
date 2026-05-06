from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.query_ai_result_service import QueryAIResultService
from app.dependencies import get_db_session

router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/tasks/{ai_task_id}/result")
async def result(ai_task_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    return success_response(await QueryAIResultService(session).result(ai_task_id), request)
