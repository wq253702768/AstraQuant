from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import BacktestResultModel

class BacktestResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def create(self, model: BacktestResultModel) -> BacktestResultModel:
        self.session.add(model); await self.session.flush(); return model
    async def get_by_task(self, task_id: str) -> BacktestResultModel | None:
        result = await self.session.execute(select(BacktestResultModel).where(BacktestResultModel.task_id == task_id))
        return result.scalar_one_or_none()
