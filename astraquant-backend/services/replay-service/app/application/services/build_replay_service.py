from app.domain.enums.replay_build_status import ReplayBuildStatus
from app.infrastructure.postgres.models import ReplayBuildTaskModel
from app.infrastructure.postgres.repositories.replay_build_task_repository import ReplayBuildTaskRepository
from app.schemas.replay_page import BuildReplayRequest, BuildReplayResponse

class BuildReplayService:
    def __init__(self, session): self.repo = ReplayBuildTaskRepository(session)
    async def create(self, payload: BuildReplayRequest) -> BuildReplayResponse:
        task = await self.repo.create(ReplayBuildTaskModel(backtest_task_id=payload.backtest_task_id, status=ReplayBuildStatus.QUEUED.value, progress=0, current_stage="queued"))
        return BuildReplayResponse(replay_build_task_id=task.id, status=task.status)
