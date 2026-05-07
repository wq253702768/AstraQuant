import asyncio

from astra_common.security import create_jwt, decode_jwt, hash_password, verify_password
from app.config import settings
from app.domain.services.login_protection_service import LoginProtectionService
from app.domain.services.token_service import TokenService


def test_password_hash():
    hashed = hash_password("password")
    assert hashed != "password"
    assert verify_password("password", hashed)


def test_jwt_roundtrip():
    token = create_jwt("u001", "secret", 60, {"roles": ["admin"]})
    payload = decode_jwt(token, "secret")
    assert payload["sub"] == "u001"
    assert payload["roles"] == ["admin"]


def test_token_service_access_token_claims():
    token = TokenService().create_access_token("u001", ["admin"], ["*"])
    payload = TokenService().decode(token)
    assert payload["sub"] == "u001"
    assert payload["token_type"] == "access"
    assert payload["roles"] == ["admin"]
    assert payload["permissions"] == ["*"]


def test_token_service_refresh_token_claims():
    token = TokenService().create_refresh_token("u001")
    payload = TokenService().decode(token)
    assert payload["sub"] == "u001"
    assert payload["token_type"] == "refresh"
    assert payload["jti"]


def test_token_hash_is_stable_and_not_plaintext():
    service = TokenService()
    token = service.create_refresh_token("u001")
    hashed = service.hash_token(token)
    assert hashed == service.hash_token(token)
    assert hashed != token
    assert len(hashed) == 64


def test_token_service_expires_at_uses_exp_claim():
    service = TokenService()
    token = service.create_refresh_token("u001")
    payload = service.decode(token)
    assert int(service.expires_at(payload).timestamp()) == payload["exp"]


class FakeRedis:
    def __init__(self):
        self.values: dict[str, str] = {}

    async def exists(self, key: str) -> int:
        return int(key in self.values)

    async def incr(self, key: str) -> int:
        self.values[key] = str(int(self.values.get(key, "0")) + 1)
        return int(self.values[key])

    async def expire(self, key: str, ttl: int) -> None:
        return None

    async def setex(self, key: str, ttl: int, value: str) -> None:
        self.values[key] = value

    async def delete(self, *keys: str) -> None:
        for key in keys:
            self.values.pop(key, None)


def test_login_protection_locks_after_limit():
    async def scenario():
        service = LoginProtectionService(FakeRedis())
        for _ in range(settings.login_failed_limit):
            count = await service.record_failure("Admin")
        assert count == settings.login_failed_limit
        assert await service.is_locked("admin")
        await service.clear("admin")
        assert not await service.is_locked("admin")

    asyncio.run(scenario())
