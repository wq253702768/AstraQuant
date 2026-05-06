from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import AITaskModel

class AITaskRepository:
    def __init__(self, session: AsyncSession): self.session = session
    async def create(self, model: AITaskModel) -> AITaskModel:
        self.session.add(model); await self.session.flush(); return model
    async def get(self, task_id: str) -> AITaskModel | None:
        result = await self.session.execute(select(AITaskModel).where(AITaskModel.id == task_id))
        return result.scalar_one_or_none()
