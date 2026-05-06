from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import BacktestTaskModel

class BacktestTaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def create(self, model: BacktestTaskModel) -> BacktestTaskModel:
        self.session.add(model); await self.session.flush(); return model
    async def get(self, task_id: str) -> BacktestTaskModel | None:
        result = await self.session.execute(select(BacktestTaskModel).where(BacktestTaskModel.id == task_id))
        return result.scalar_one_or_none()
