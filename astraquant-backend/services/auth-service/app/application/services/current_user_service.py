from astra_common.errors import AppError, ErrorCode
from app.domain.services.token_service import TokenService
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.user import CurrentUserResponse

class CurrentUserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.token_service = TokenService()

    async def get_current_user(self, token: str) -> CurrentUserResponse:
        payload = self.token_service.decode(token)
        if payload.get("token_type") != "access":
            raise AppError(ErrorCode.UNAUTHORIZED, "Access Token 无效", 401)
        user = await self.user_repository.get_by_id(str(payload["sub"]))
        if user is None or not user.active:
            raise AppError(ErrorCode.UNAUTHORIZED, "用户不存在或已禁用", 401)
        return CurrentUserResponse(id=user.id, username=user.username, display_name=user.display_name, roles=user.roles, permissions=user.permissions)
