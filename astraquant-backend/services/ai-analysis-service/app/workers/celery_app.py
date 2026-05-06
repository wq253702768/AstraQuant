from celery import Celery
from app.config import settings

celery_app = Celery("ai_analysis_service", broker=settings.redis_url, backend=settings.redis_url.replace("/0", "/4"))
celery_app.conf.task_default_queue = "ai_analysis"
