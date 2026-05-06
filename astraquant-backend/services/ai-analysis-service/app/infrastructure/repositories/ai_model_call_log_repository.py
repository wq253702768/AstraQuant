from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import AIModelCallLogModel

class AIModelCallLogRepository:
    def __init__(self, session: AsyncSession): self.session = session
    async def create(self, model: AIModelCallLogModel) -> AIModelCallLogModel:
        self.session.add(model); await self.session.flush(); return model
    async def list_by_task(self, task_id: str) -> list[AIModelCallLogModel]:
        result = await self.session.execute(select(AIModelCallLogModel).where(AIModelCallLogModel.ai_task_id == task_id).order_by(AIModelCallLogModel.created_at.asc()))
        return list(result.scalars())
