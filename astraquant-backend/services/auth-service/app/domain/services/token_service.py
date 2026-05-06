from astra_common.security import create_jwt, decode_jwt
from app.config import settings

class TokenService:
    def create_access_token(self, user_id: str, roles: list[str], permissions: list[str]) -> str:
        return create_jwt(user_id, settings.jwt_secret, settings.jwt_access_expire_seconds, {"token_type": "access", "roles": roles, "permissions": permissions})
    def create_refresh_token(self, user_id: str) -> str:
        return create_jwt(user_id, settings.jwt_secret, settings.jwt_refresh_expire_seconds, {"token_type": "refresh"})
    def decode(self, token: str) -> dict:
        return decode_jwt(token, settings.jwt_secret)
