from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from astra_common.response import success_response
from app.application.services.change_password_service import ChangePasswordService
from app.application.services.current_user_service import CurrentUserService
from app.application.services.login_service import LoginService
from app.application.services.logout_service import LogoutService
from app.application.services.refresh_token_service import RefreshTokenService
from app.dependencies import get_bearer_token, get_user_repository
from app.infrastructure.db.session import get_session
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.auth import ChangePasswordRequest, LoginRequest, LogoutRequest, RefreshTokenRequest

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(payload: LoginRequest, request: Request, session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    result = await LoginService(repository).login(payload.username, payload.password, request.client.host if request.client else None, request.headers.get("user-agent"))
    await session.commit()
    return success_response(result, request)

@router.post("/refresh")
async def refresh(payload: RefreshTokenRequest, request: Request, session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    result = await RefreshTokenService(repository).refresh(payload.refresh_token, request.client.host if request.client else None, request.headers.get("user-agent"), getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)

@router.get("/me")
async def me(request: Request, token: str = Depends(get_bearer_token), repository: UserRepository = Depends(get_user_repository)):
    result = await CurrentUserService(repository).get_current_user(token)
    return success_response(result, request)

@router.post("/logout")
async def logout(payload: LogoutRequest, request: Request, token: str = Depends(get_bearer_token), session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    result = await LogoutService(repository).logout(token, payload.refresh_token, request.client.host if request.client else None, request.headers.get("user-agent"), getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)

@router.put("/password")
async def change_password(payload: ChangePasswordRequest, request: Request, token: str = Depends(get_bearer_token), session: AsyncSession = Depends(get_session)):
    repository = UserRepository(session)
    result = await ChangePasswordService(repository).change_password(token, payload.old_password, payload.new_password, request.client.host if request.client else None, request.headers.get("user-agent"), getattr(request.state, "trace_id", None))
    await session.commit()
    return success_response(result, request)
