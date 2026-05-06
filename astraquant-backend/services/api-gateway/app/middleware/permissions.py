from fastapi import Request

from astra_common.errors import AppError, ErrorCode


def require_permission(request: Request, permission: str) -> None:
    user = getattr(request.state, "user", None) or {}
    permissions = set(user.get("permissions", []))
    if "*" in permissions or permission in permissions:
        return
    raise AppError(ErrorCode.FORBIDDEN, "无权限访问该资源", 403, {"permission": permission})
