from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import StrategyScoreModel

class StrategyScoreRepository:
    def __init__(self, session: AsyncSession): self.session = session
    async def create(self, model: StrategyScoreModel) -> StrategyScoreModel:
        self.session.add(model); await self.session.flush(); return model
    async def get(self, score_id: str) -> StrategyScoreModel | None:
        result = await self.session.execute(select(StrategyScoreModel).where(StrategyScoreModel.id == score_id))
        return result.scalar_one_or_none()
    async def latest_by_version(self, strategy_version_id: str) -> StrategyScoreModel | None:
        result = await self.session.execute(select(StrategyScoreModel).where(StrategyScoreModel.strategy_version_id == strategy_version_id).order_by(StrategyScoreModel.created_at.desc()).limit(1))
        return result.scalar_one_or_none()
