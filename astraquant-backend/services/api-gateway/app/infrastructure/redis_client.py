try:
    import redis.asyncio as redis
except Exception:  # pragma: no cover
    redis = None

from app.config import settings


def create_redis_client():
    if redis is None:
        return None
    return redis.from_url(settings.redis_url, decode_responses=True)
