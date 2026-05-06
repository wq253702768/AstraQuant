from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import ReportFileModel
class ReportFileRepository:
    def __init__(self, session: AsyncSession): self.session=session
    async def create(self, model: ReportFileModel): self.session.add(model); await self.session.flush(); return model
    async def list_by_task(self, task_id: str):
        result=await self.session.execute(select(ReportFileModel).where(ReportFileModel.report_task_id==task_id)); return list(result.scalars())
