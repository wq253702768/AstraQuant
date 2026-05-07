from datetime import datetime, timezone

from app.application.services.sync_klines_service import SyncKlinesService
from app.domain.enums.sync_status import SyncStatus
from app.infrastructure.repositories.sync_task_repository import SyncTaskRepository

class RunSyncTaskService:
    def __init__(self, session):
        self.session = session
        self.repo = SyncTaskRepository(session)

    async def run(self, task_id: str):
        task = await self.repo.get(task_id)
        if not task:
            return None
        task.status = SyncStatus.RUNNING.value
        task.current_stage = "syncing"
        task.progress = 10
        await self.session.flush()
        try:
            inserted, updated = await SyncKlinesService(self.session).sync_task(task)
            task.status = SyncStatus.SUCCESS.value
            task.current_stage = "completed"
            task.progress = 100
            task.error_message = None
            task.updated_at = datetime.now(timezone.utc)
            task.current_stage = f"inserted={inserted},updated={updated}"
            return task, inserted, updated
        except Exception as exc:
            task.status = SyncStatus.FAILED.value
            task.current_stage = "failed"
            task.error_message = str(exc)
            raise
