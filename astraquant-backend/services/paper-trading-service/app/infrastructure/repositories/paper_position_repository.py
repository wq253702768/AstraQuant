from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import PaperPositionModel
class PaperPositionRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def create(self, model: PaperPositionModel): self.session.add(model); await self.session.flush(); return model
    async def get(self, item_id: str):
        result=await self.session.execute(select(PaperPositionModel).where(PaperPositionModel.id==item_id)); return result.scalar_one_or_none()
    async def list(self):
        result=await self.session.execute(select(PaperPositionModel)); return list(result.scalars())
