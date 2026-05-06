from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.errors import AppError
from astra_common.response import success_response
from app.application.services.create_sync_task_service import CreateSyncTaskService
from app.dependencies import get_db_session, get_operator_id
from app.infrastructure.repositories.sync_task_repository import SyncTaskRepository
from app.schemas.sync import CreateSyncTaskRequest, SyncTaskStatusResponse

router = APIRouter(prefix="/market-data/sync", tags=["market-data-sync"])

@router.post("")
async def create_sync_task(payload: CreateSyncTaskRequest, request: Request, session: AsyncSession = Depends(get_db_session), operator_id: str | None = Depends(get_operator_id)):
    result = await CreateSyncTaskService(session).execute(payload, operator_id)
    await session.commit()
    return success_response(result, request)

@router.get("/{sync_task_id}")
async def get_sync_task(sync_task_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    task = await SyncTaskRepository(session).get(sync_task_id)
    if not task:
        raise AppError("MARKET_DATA_SYNC_TASK_NOT_FOUND", "同步任务不存在", 404)
    return success_response(SyncTaskStatusResponse(sync_task_id=task.id, status=task.status, progress=float(task.progress), current_stage=task.current_stage, error_message=task.error_message), request)
