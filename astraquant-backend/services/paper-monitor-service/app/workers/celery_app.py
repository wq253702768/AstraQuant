from celery import Celery
from app.config import settings
celery_app=Celery("paper_monitor_service", broker=settings.redis_url, backend=settings.redis_url.replace("/0","/6"))
celery_app.conf.task_default_queue="paper_monitor"
