from datetime import UTC, datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import User
from app.domain.services.permission_service import permissions_for_roles
from app.infrastructure.db.models import AuditEventBasicModel, LoginLogModel, RefreshTokenModel, RoleModel, UserAccountModel, UserRoleModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> tuple[UserAccountModel, User] | None:
        result = await self.session.execute(select(UserAccountModel).where(UserAccountModel.username == username))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        roles = await self._role_codes(model.id)
        user = User(id=str(model.id), username=model.username, display_name=model.display_name, status=model.status, roles=roles, permissions=permissions_for_roles(roles))
        return model, user

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self.session.execute(select(UserAccountModel).where(UserAccountModel.id == user_id))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        roles = await self._role_codes(model.id)
        return User(id=str(model.id), username=model.username, display_name=model.display_name, status=model.status, roles=roles, permissions=permissions_for_roles(roles))

    async def _role_codes(self, user_id: str) -> list[str]:
        roles_result = await self.session.execute(select(RoleModel.code).join(UserRoleModel, UserRoleModel.role_id == RoleModel.id).where(UserRoleModel.user_id == user_id))
        return list(roles_result.scalars())

    async def touch_last_login(self, user_id: str) -> None:
        await self.session.execute(update(UserAccountModel).where(UserAccountModel.id == user_id).values(last_login_at=datetime.now(UTC)))

    async def write_login_log(self, username: str, success: bool, user_id: str | None = None, failure_reason: str | None = None, ip_address: str | None = None, user_agent: str | None = None) -> None:
        self.session.add(LoginLogModel(user_id=user_id, username=username, success=success, failure_reason=failure_reason, ip_address=ip_address, user_agent=user_agent))

    async def get_account_by_id(self, user_id: str) -> UserAccountModel | None:
        result = await self.session.execute(select(UserAccountModel).where(UserAccountModel.id == user_id))
        return result.scalar_one_or_none()

    async def update_password_hash(self, user_id: str, password_hash: str) -> None:
        await self.session.execute(update(UserAccountModel).where(UserAccountModel.id == user_id).values(password_hash=password_hash, updated_at=datetime.now(UTC)))

    async def save_refresh_token(self, user_id: str, token_hash: str, expires_at: datetime, ip_address: str | None = None, user_agent: str | None = None) -> None:
        self.session.add(RefreshTokenModel(user_id=user_id, token_hash=token_hash, expires_at=expires_at, ip_address=ip_address, user_agent=user_agent))

    async def get_refresh_token(self, token_hash: str) -> RefreshTokenModel | None:
        result = await self.session.execute(select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash))
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, token_hash: str) -> None:
        await self.session.execute(update(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash, RefreshTokenModel.revoked_at.is_(None)).values(revoked_at=datetime.now(UTC)))

    async def revoke_all_refresh_tokens(self, user_id: str) -> None:
        await self.session.execute(update(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id, RefreshTokenModel.revoked_at.is_(None)).values(revoked_at=datetime.now(UTC)))

    async def write_audit_event(self, event_type: str, action: str, actor_id: str | None = None, actor_username: str | None = None, resource_type: str | None = None, resource_id: str | None = None, metadata_json: dict | None = None, ip_address: str | None = None, user_agent: str | None = None, trace_id: str | None = None) -> None:
        self.session.add(AuditEventBasicModel(event_type=event_type, actor_id=actor_id, actor_username=actor_username, resource_type=resource_type, resource_id=resource_id, action=action, metadata_json=metadata_json, ip_address=ip_address, user_agent=user_agent, trace_id=trace_id))
