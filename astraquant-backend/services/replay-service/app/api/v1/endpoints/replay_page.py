from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.errors import AppError
from astra_common.response import success_response
from app.application.services.build_replay_service import BuildReplayService
from app.application.services.query_replay_page_service import QueryReplayPageService
from app.dependencies import get_db_session
from app.infrastructure.postgres.repositories.replay_build_task_repository import ReplayBuildTaskRepository
from app.schemas.replay_page import BuildReplayRequest

router = APIRouter(prefix="/replays", tags=["replays"])

@router.post("/build")
async def build(payload: BuildReplayRequest, request: Request, session: AsyncSession = Depends(get_db_session)):
    result = await BuildReplayService(session).create(payload)
    await session.commit()
    return success_response(result, request)

@router.get("/build/{replay_build_task_id}")
async def build_status(replay_build_task_id: str, request: Request, session: AsyncSession = Depends(get_db_session)):
    task = await ReplayBuildTaskRepository(session).get(replay_build_task_id)
    if not task: raise AppError("REPLAY_BUILD_TASK_NOT_FOUND", "回放构建任务不存在", 404)
    return success_response({"replay_build_task_id": task.id, "backtest_task_id": task.backtest_task_id, "status": task.status, "progress": float(task.progress), "current_stage": task.current_stage}, request)

@router.get("/{drawdown_id}/page")
async def page(drawdown_id: str, request: Request):
    return success_response(await QueryReplayPageService().execute(drawdown_id), request)
