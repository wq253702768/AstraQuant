from typing import Annotated
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.postgres.session import get_session
async def get_db_session(session: AsyncSession = Depends(get_session)) -> AsyncSession: return session
def get_operator_id(x_user_id: Annotated[str | None, Header(alias="X-User-Id")] = None) -> str | None: return x_user_id
