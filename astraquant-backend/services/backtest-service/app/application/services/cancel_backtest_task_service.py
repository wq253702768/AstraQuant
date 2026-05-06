from astra_common.errors import AppError
from app.domain.enums.backtest_status import BacktestStatus
from app.infrastructure.repositories.backtest_task_repository import BacktestTaskRepository

class CancelBacktestTaskService:
    def __init__(self, session):
        self.repo = BacktestTaskRepository(session)
    async def execute(self, task_id: str):
        task = await self.repo.get(task_id)
        if not task:
            raise AppError("BACKTEST_TASK_NOT_FOUND", "回测任务不存在", 404)
        if task.status not in {BacktestStatus.QUEUED.value, BacktestStatus.RUNNING.value}:
            raise AppError("BACKTEST_CANNOT_CANCEL", "当前状态不可取消", 409)
        task.status = BacktestStatus.CANCELED.value
        return {"task_id": task.id, "status": task.status}
