from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models import StrategyVersionModel

class StrategyVersionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: StrategyVersionModel) -> StrategyVersionModel:
        self.session.add(model)
        await self.session.flush()
        return model

    async def get(self, version_id: str) -> StrategyVersionModel | None:
        result = await self.session.execute(select(StrategyVersionModel).where(StrategyVersionModel.id == version_id))
        return result.scalar_one_or_none()

    async def list_by_strategy(self, strategy_id: str) -> list[StrategyVersionModel]:
        result = await self.session.execute(select(StrategyVersionModel).where(StrategyVersionModel.strategy_id == strategy_id).order_by(StrategyVersionModel.created_at.asc()))
        return list(result.scalars())

    async def version_strings(self, strategy_id: str) -> list[str]:
        result = await self.session.execute(select(StrategyVersionModel.version).where(StrategyVersionModel.strategy_id == strategy_id))
        return list(result.scalars())
