from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from astra_common.errors import AppError, ErrorCode
from astra_common.response import error_response
from astra_common.security import decode_jwt
from app.config import settings
from app.infrastructure.redis_client import create_redis_client

PUBLIC_PATHS = {"/health", "/api/auth/login", "/api/auth/refresh", "/docs", "/openapi.json", "/redoc"}
PUBLIC_PREFIXES = ("/api/ws/",)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = getattr(request.state, "trace_id", None)
        if request.url.path in PUBLIC_PATHS or request.url.path.startswith(PUBLIC_PREFIXES):
            return await call_next(request)
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            return JSONResponse(status_code=401, content=error_response(ErrorCode.UNAUTHORIZED.value, "缺少 Authorization Bearer Token", trace_id).model_dump())
        token = authorization.removeprefix("Bearer ").strip()
        try:
            payload = decode_jwt(token, settings.jwt_secret)
        except AppError as exc:
            return JSONResponse(status_code=exc.status_code, content=error_response(exc.code, exc.message, trace_id).model_dump())
        if payload.get("token_type") != "access":
            return JSONResponse(status_code=401, content=error_response(ErrorCode.UNAUTHORIZED.value, "Access Token 无效", trace_id).model_dump())
        if await self._blacklisted(payload):
            return JSONResponse(status_code=401, content=error_response(ErrorCode.UNAUTHORIZED.value, "Token 已失效", trace_id).model_dump())
        request.state.user = {"id": payload.get("sub"), "roles": payload.get("roles", []), "permissions": payload.get("permissions", [])}
        return await call_next(request)

    async def _blacklisted(self, payload: dict) -> bool:
        if not payload.get("jti"):
            return False
        client = create_redis_client()
        if client is None:
            return False
        try:
            return bool(await client.exists(f"auth:blacklist:access:{payload['jti']}"))
        finally:
            await client.aclose()
