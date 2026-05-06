from datetime import UTC, datetime
from hashlib import sha256
from uuid import uuid4

from astra_common.security import create_jwt, decode_jwt
from app.config import settings


class TokenService:
    def create_access_token(self, user_id: str, roles: list[str], permissions: list[str]) -> str:
        return create_jwt(user_id, settings.jwt_secret, settings.jwt_access_expire_seconds, {"token_type": "access", "roles": roles, "permissions": permissions, "jti": str(uuid4())})
    def create_refresh_token(self, user_id: str) -> str:
        return create_jwt(user_id, settings.jwt_secret, settings.jwt_refresh_expire_seconds, {"token_type": "refresh", "jti": str(uuid4())})
    def decode(self, token: str) -> dict:
        return decode_jwt(token, settings.jwt_secret)
    def hash_token(self, token: str) -> str:
        return sha256(token.encode("utf-8")).hexdigest()
    def ttl_seconds(self, payload: dict) -> int:
        return max(0, int(payload.get("exp", 0)) - int(datetime.now(UTC).timestamp()))
