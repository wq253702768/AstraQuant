from app.infrastructure.redis.client import create_redis_client


class AccessTokenBlacklist:
    def __init__(self):
        self.redis = create_redis_client()

    async def add(self, jti: str | None, ttl_seconds: int) -> None:
        if not jti or ttl_seconds <= 0 or self.redis is None:
            return
        await self.redis.setex(f"auth:blacklist:access:{jti}", ttl_seconds, "1")

    async def contains(self, jti: str | None) -> bool:
        if not jti or self.redis is None:
            return False
        return bool(await self.redis.get(f"auth:blacklist:access:{jti}"))
