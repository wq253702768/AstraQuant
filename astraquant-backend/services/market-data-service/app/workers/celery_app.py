from celery import Celery
from app.config import settings

celery_app = Celery(
    "market_data_service",
    broker=settings.redis_url,
    backend=settings.redis_url.replace("/0", "/1"),
)
celery_app.conf.task_default_queue = "market_data"
