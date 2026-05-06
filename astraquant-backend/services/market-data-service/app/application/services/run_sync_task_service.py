from app.domain.enums.sync_status import SyncStatus
from app.infrastructure.repositories.sync_task_repository import SyncTaskRepository

class RunSyncTaskService:
    def __init__(self, session):
        self.repo = SyncTaskRepository(session)

    async def mark_running(self, task_id: str):
        task = await self.repo.get(task_id)
        if task:
            task.status = SyncStatus.RUNNING.value
            task.current_stage = "running"
            task.progress = 10
        return task
