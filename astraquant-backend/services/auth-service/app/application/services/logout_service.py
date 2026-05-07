from astra_common.errors import AppError, ErrorCode
from app.domain.services.access_token_blacklist import AccessTokenBlacklist
from app.domain.services.token_service import TokenService
from app.infrastructure.repositories.user_repository import UserRepository


class LogoutService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.token_service = TokenService()
        self.blacklist = AccessTokenBlacklist()

    async def logout(self, access_token: str, refresh_token: str, ip_address: str | None = None, user_agent: str | None = None, trace_id: str | None = None) -> dict:
        payload = self.token_service.decode(access_token)
        if payload.get("token_type") != "access":
            raise AppError(ErrorCode.UNAUTHORIZED, "Access Token 无效", 401)
        refresh_payload = self.token_service.decode(refresh_token)
        if refresh_payload.get("token_type") != "refresh":
            raise AppError(ErrorCode.UNAUTHORIZED, "Refresh Token 无效", 401)
        token_hash = self.token_service.hash_token(refresh_token)
        await self.user_repository.revoke_refresh_token(token_hash)
        await self.blacklist.add(payload.get("jti"), self.token_service.ttl_seconds(payload))
        user = await self.user_repository.get_by_id(str(payload["sub"]))
        await self.user_repository.write_audit_event(
            "USER_LOGOUT",
            "LOGOUT",
            actor_id=str(payload["sub"]),
            actor_username=user.username if user else None,
            resource_type="user_account",
            resource_id=str(payload["sub"]),
            ip_address=ip_address,
            user_agent=user_agent,
            trace_id=trace_id,
        )
        return {"success": True}
