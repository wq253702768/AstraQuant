from datetime import UTC, datetime

from astra_common.errors import AppError, ErrorCode
from app.config import settings
from app.domain.services.token_service import TokenService
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.auth import RefreshTokenResponse

class RefreshTokenService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.token_service = TokenService()

    async def refresh(self, refresh_token: str, ip_address: str | None = None, user_agent: str | None = None, trace_id: str | None = None) -> RefreshTokenResponse:
        payload = self.token_service.decode(refresh_token)
        if payload.get("token_type") != "refresh":
            raise AppError(ErrorCode.UNAUTHORIZED, "Refresh Token 无效", 401)
        token_hash = self.token_service.hash_token(refresh_token)
        token_record = await self.user_repository.get_refresh_token(token_hash)
        if token_record is None or token_record.revoked_at is not None or token_record.expires_at <= datetime.now(UTC):
            raise AppError(ErrorCode.UNAUTHORIZED, "Refresh Token 无效或已撤销", 401)
        user = await self.user_repository.get_by_id(str(payload["sub"]))
        if user is None or not user.active:
            raise AppError(ErrorCode.UNAUTHORIZED, "用户不存在或已禁用", 401)
        await self.user_repository.revoke_refresh_token(token_hash)
        new_refresh_token = self.token_service.create_refresh_token(user.id)
        new_refresh_payload = self.token_service.decode(new_refresh_token)
        await self.user_repository.save_refresh_token(
            user.id,
            self.token_service.hash_token(new_refresh_token),
            datetime.fromtimestamp(int(new_refresh_payload["exp"]), UTC),
            ip_address,
            user_agent,
        )
        await self.user_repository.write_audit_event("TOKEN_REFRESHED", "TOKEN_REFRESH", actor_id=user.id, actor_username=user.username, ip_address=ip_address, user_agent=user_agent, trace_id=trace_id)
        return RefreshTokenResponse(access_token=self.token_service.create_access_token(user.id, user.roles, user.permissions), refresh_token=new_refresh_token, expires_in=settings.jwt_access_expire_seconds)
