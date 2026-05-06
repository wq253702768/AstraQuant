from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.current_user_service import CurrentUserService
from app.application.services.login_service import LoginService
from app.application.services.refresh_token_service import RefreshTokenService
from app.dependencies import get_bearer_token, get_user_repository
from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(payload: LoginRequest, request: Request, session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    result = await LoginService(repository).login(payload.username, payload.password, request.client.host if request.client else None, request.headers.get("user-agent"))
    await session.commit()
    return success_response(result, request)

@router.post("/refresh")
async def refresh(payload: RefreshTokenRequest, request: Request, repository: UserRepository = Depends(get_user_repository)):
    result = await RefreshTokenService(repository).refresh(payload.refresh_token)
    return success_response(result, request)

@router.get("/me")
async def me(request: Request, token: str = Depends(get_bearer_token), repository: UserRepository = Depends(get_user_repository)):
    result = await CurrentUserService(repository).get_current_user(token)
    return success_response(result, request)
