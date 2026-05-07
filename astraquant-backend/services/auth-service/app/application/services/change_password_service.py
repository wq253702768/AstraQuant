from astra_common.errors import AppError, ErrorCode
from app.domain.services.access_token_blacklist import AccessTokenBlacklist
from app.domain.services.password_service import PasswordService
from app.domain.services.token_service import TokenService
from app.infrastructure.repositories.user_repository import UserRepository


class ChangePasswordService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_service = PasswordService()
        self.token_service = TokenService()
        self.blacklist = AccessTokenBlacklist()

    async def change_password(
        self,
        access_token: str,
        old_password: str,
        new_password: str,
        ip_address: str | None = None,
        user_agent: str | None = None,
        trace_id: str | None = None,
    ) -> dict:
        payload = self.token_service.decode(access_token)
        if payload.get("token_type") != "access":
            raise AppError(ErrorCode.UNAUTHORIZED, "Access Token 无效", 401)
        user_id = str(payload["sub"])
        account = await self.user_repository.get_account_by_id(user_id)
        if account is None:
            raise AppError(ErrorCode.UNAUTHORIZED, "用户不存在", 401)
        if not self.password_service.verify(old_password, account.password_hash):
            await self.user_repository.write_audit_event(
                "PASSWORD_CHANGE_FAILED",
                "CHANGE_PASSWORD",
                actor_id=user_id,
                actor_username=account.username,
                resource_type="user_account",
                resource_id=user_id,
                metadata_json={"reason": "OLD_PASSWORD_INCORRECT"},
                ip_address=ip_address,
                user_agent=user_agent,
                trace_id=trace_id,
            )
            raise AppError("AUTH_PASSWORD_INCORRECT", "原密码错误", 400)
        self._validate_password(new_password)
        await self.user_repository.update_password_hash(user_id, self.password_service.hash(new_password))
        await self.user_repository.revoke_all_refresh_tokens(user_id)
        await self.blacklist.add(payload.get("jti"), self.token_service.ttl_seconds(payload))
        await self.user_repository.write_audit_event(
            "PASSWORD_CHANGED",
            "CHANGE_PASSWORD",
            actor_id=user_id,
            actor_username=account.username,
            resource_type="user_account",
            resource_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            trace_id=trace_id,
        )
        return {"success": True}

    @staticmethod
    def _validate_password(password: str) -> None:
        if (
            len(password) < 8
            or not any(ch.islower() for ch in password)
            or not any(ch.isupper() for ch in password)
            or not any(ch.isdigit() for ch in password)
            or not any(not ch.isalnum() for ch in password)
        ):
            raise AppError("AUTH_PASSWORD_TOO_WEAK", "新密码不符合复杂度要求", 400)
