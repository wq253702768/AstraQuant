from astra_common.errors import AppError, ErrorCode
from app.config import settings
from app.domain.services.login_protection_service import LoginProtectionService
from app.domain.services.password_service import PasswordService
from app.domain.services.token_service import TokenService
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponse, UserTokenInfo

class LoginService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_service = PasswordService()
        self.token_service = TokenService()
        self.login_protection = LoginProtectionService()

    async def login(self, username: str, password: str, ip_address: str | None, user_agent: str | None) -> LoginResponse:
        if await self.login_protection.is_locked(username):
            await self.user_repository.write_audit_event("LOGIN_LOCKED", "LOGIN", actor_username=username, metadata_json={"reason": "LOCKED"}, ip_address=ip_address, user_agent=user_agent)
            raise AppError("AUTH_USER_LOCKED", "登录失败次数过多，请稍后再试", 423)
        record = await self.user_repository.get_by_username(username)
        if record is None:
            await self.user_repository.write_login_log(username, False, failure_reason="USER_NOT_FOUND", ip_address=ip_address, user_agent=user_agent)
            failed_count = await self.login_protection.record_failure(username)
            await self.user_repository.write_audit_event("USER_LOGIN_FAILED", "LOGIN", actor_username=username, metadata_json={"reason": "USER_NOT_FOUND", "failed_count": failed_count}, ip_address=ip_address, user_agent=user_agent)
            if failed_count >= settings.login_failed_limit:
                await self.user_repository.write_audit_event("LOGIN_LOCKED", "LOGIN_LOCKED", actor_username=username, metadata_json={"failed_count": failed_count, "lock_seconds": settings.login_lock_seconds}, ip_address=ip_address, user_agent=user_agent)
                raise AppError("AUTH_USER_LOCKED", "登录失败次数过多，请稍后再试", 423)
            raise AppError("AUTH_INVALID_CREDENTIALS", "用户名或密码错误", 401)
        model, user = record
        if not user.active:
            await self.user_repository.write_login_log(username, False, user_id=user.id, failure_reason="USER_DISABLED", ip_address=ip_address, user_agent=user_agent)
            raise AppError(ErrorCode.FORBIDDEN, "用户已被禁用", 403)
        if not self.password_service.verify(password, model.password_hash):
            await self.user_repository.write_login_log(username, False, user_id=user.id, failure_reason="WRONG_PASSWORD", ip_address=ip_address, user_agent=user_agent)
            failed_count = await self.login_protection.record_failure(username)
            await self.user_repository.write_audit_event("USER_LOGIN_FAILED", "LOGIN", actor_id=user.id, actor_username=username, resource_type="user_account", resource_id=user.id, metadata_json={"reason": "WRONG_PASSWORD", "failed_count": failed_count}, ip_address=ip_address, user_agent=user_agent)
            if failed_count >= settings.login_failed_limit:
                await self.user_repository.write_audit_event("LOGIN_LOCKED", "LOGIN_LOCKED", actor_id=user.id, actor_username=username, resource_type="user_account", resource_id=user.id, metadata_json={"failed_count": failed_count, "lock_seconds": settings.login_lock_seconds}, ip_address=ip_address, user_agent=user_agent)
                raise AppError("AUTH_USER_LOCKED", "登录失败次数过多，请稍后再试", 423)
            raise AppError("AUTH_INVALID_CREDENTIALS", "用户名或密码错误", 401)
        await self.login_protection.clear(username)
        access_token = self.token_service.create_access_token(user.id, user.roles, user.permissions)
        refresh_token = self.token_service.create_refresh_token(user.id)
        refresh_payload = self.token_service.decode(refresh_token)
        await self.user_repository.save_refresh_token(user.id, self.token_service.hash_token(refresh_token), self.token_service.expires_at(refresh_payload), ip_address, user_agent)
        await self.user_repository.touch_last_login(user.id)
        await self.user_repository.write_login_log(username, True, user_id=user.id, ip_address=ip_address, user_agent=user_agent)
        await self.user_repository.write_audit_event("USER_LOGIN", "LOGIN", actor_id=user.id, actor_username=username, resource_type="user_account", resource_id=user.id, ip_address=ip_address, user_agent=user_agent)
        return LoginResponse(access_token=access_token, refresh_token=refresh_token, expires_in=settings.jwt_access_expire_seconds, user=UserTokenInfo(id=user.id, username=user.username, display_name=user.display_name, roles=user.roles))
