from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import SignalEventModel
class SignalEventRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def create(self, model: SignalEventModel): self.session.add(model); await self.session.flush(); return model
    async def get(self, signal_id: str):
        result=await self.session.execute(select(SignalEventModel).where(SignalEventModel.id==signal_id)); return result.scalar_one_or_none()
    async def list(self, page:int=1, page_size:int=20):
        total=(await self.session.execute(select(func.count()).select_from(SignalEventModel))).scalar_one()
        rows=(await self.session.execute(select(SignalEventModel).order_by(SignalEventModel.created_at.desc()).offset((page-1)*page_size).limit(page_size))).scalars()
        return list(rows), int(total)
