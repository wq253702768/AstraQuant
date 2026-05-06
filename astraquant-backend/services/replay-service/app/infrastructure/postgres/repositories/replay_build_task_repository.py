from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import ReplayBuildTaskModel

class ReplayBuildTaskRepository:
    def __init__(self, session: AsyncSession): self.session = session
    async def create(self, model: ReplayBuildTaskModel) -> ReplayBuildTaskModel:
        self.session.add(model); await self.session.flush(); return model
    async def get(self, task_id: str) -> ReplayBuildTaskModel | None:
        result = await self.session.execute(select(ReplayBuildTaskModel).where(ReplayBuildTaskModel.id == task_id))
        return result.scalar_one_or_none()
