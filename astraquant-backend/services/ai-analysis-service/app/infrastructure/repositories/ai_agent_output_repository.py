from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import AIAgentOutputModel

class AIAgentOutputRepository:
    def __init__(self, session: AsyncSession): self.session = session
    async def create(self, model: AIAgentOutputModel) -> AIAgentOutputModel:
        self.session.add(model); await self.session.flush(); return model
    async def list_by_task(self, task_id: str) -> list[AIAgentOutputModel]:
        result = await self.session.execute(select(AIAgentOutputModel).where(AIAgentOutputModel.ai_task_id == task_id).order_by(AIAgentOutputModel.created_at.asc()))
        return list(result.scalars())
