from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import StrategyRuntimeStateModel
class StrategyRuntimeRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def list(self):
        result=await self.session.execute(select(StrategyRuntimeStateModel).order_by(StrategyRuntimeStateModel.updated_at.desc())); return list(result.scalars())
