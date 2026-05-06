from astra_common.errors import AppError
from app.infrastructure.repositories.backtest_task_repository import BacktestTaskRepository
from app.schemas.backtest import BacktestStatusResponse

class QueryBacktestStatusService:
    def __init__(self, session):
        self.repo = BacktestTaskRepository(session)
    async def execute(self, task_id: str) -> BacktestStatusResponse:
        task = await self.repo.get(task_id)
        if not task:
            raise AppError("BACKTEST_TASK_NOT_FOUND", "回测任务不存在", 404)
        return BacktestStatusResponse(task_id=task.id, status=task.status, progress=float(task.progress), current_stage=task.current_stage, processed_bars=task.processed_bars, total_bars=task.total_bars, error_message=task.error_message)
