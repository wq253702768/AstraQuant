from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import MarketDataSyncTaskModel

class SyncTaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: MarketDataSyncTaskModel) -> MarketDataSyncTaskModel:
        self.session.add(model)
        await self.session.flush()
        return model

    async def get(self, task_id: str) -> MarketDataSyncTaskModel | None:
        result = await self.session.execute(select(MarketDataSyncTaskModel).where(MarketDataSyncTaskModel.id == task_id))
        return result.scalar_one_or_none()
