from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models import StrategyStatusLogModel

class StrategyStatusLogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: StrategyStatusLogModel) -> StrategyStatusLogModel:
        self.session.add(model)
        await self.session.flush()
        return model
