from app.config import settings
from app.infrastructure.redis.client import create_redis_client


class LoginProtectionService:
    def __init__(self, redis_client=None):
        self.redis = redis_client if redis_client is not None else create_redis_client()

    def failed_key(self, username: str) -> str:
        return f"auth:login_failed:{username.lower()}"

    def locked_key(self, username: str) -> str:
        return f"auth:login_locked:{username.lower()}"

    async def is_locked(self, username: str) -> bool:
        if self.redis is None:
            return False
        return bool(await self.redis.exists(self.locked_key(username)))

    async def record_failure(self, username: str) -> int:
        if self.redis is None:
            return 0
        key = self.failed_key(username)
        count = int(await self.redis.incr(key))
        if count == 1:
            await self.redis.expire(key, settings.login_failed_window_seconds)
        if count >= settings.login_failed_limit:
            await self.redis.setex(self.locked_key(username), settings.login_lock_seconds, "1")
        return count

    async def clear(self, username: str) -> None:
        if self.redis is None:
            return
        await self.redis.delete(self.failed_key(username), self.locked_key(username))
