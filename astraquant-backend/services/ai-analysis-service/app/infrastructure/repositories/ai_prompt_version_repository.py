from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.models import AIPromptVersionModel

class AIPromptVersionRepository:
    def __init__(self, session: AsyncSession): self.session = session
    async def list_enabled(self) -> list[AIPromptVersionModel]:
        result = await self.session.execute(select(AIPromptVersionModel).where(AIPromptVersionModel.enabled.is_(True)).order_by(AIPromptVersionModel.agent_name.asc()))
        return list(result.scalars())
