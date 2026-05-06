from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import ReportTaskModel
class ReportTaskRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def create(self, model: ReportTaskModel): self.session.add(model); await self.session.flush(); return model
    async def get(self, task_id: str):
        result=await self.session.execute(select(ReportTaskModel).where(ReportTaskModel.id==task_id)); return result.scalar_one_or_none()
