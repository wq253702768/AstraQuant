from astra_common.errors import AppError, ErrorCode
from app.config import settings
from app.domain.services.token_service import TokenService
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.auth import RefreshTokenResponse

class RefreshTokenService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.token_service = TokenService()

    async def refresh(self, refresh_token: str) -> RefreshTokenResponse:
        payload = self.token_service.decode(refresh_token)
        if payload.get("token_type") != "refresh":
            raise AppError(ErrorCode.UNAUTHORIZED, "Refresh Token 无效", 401)
        user = await self.user_repository.get_by_id(str(payload["sub"]))
        if user is None or not user.active:
            raise AppError(ErrorCode.UNAUTHORIZED, "用户不存在或已禁用", 401)
        return RefreshTokenResponse(access_token=self.token_service.create_access_token(user.id, user.roles, user.permissions), expires_in=settings.jwt_access_expire_seconds)
