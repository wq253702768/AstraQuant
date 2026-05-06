from typing import Annotated
from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.errors import AppError, ErrorCode
from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.user_repository import UserRepository

async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

def get_bearer_token(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise AppError(ErrorCode.UNAUTHORIZED, "缺少 Authorization Bearer Token", 401)
    return authorization.removeprefix("Bearer ").strip()
