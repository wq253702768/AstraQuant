import json
import logging
from app.config import settings
logger = logging.getLogger(__name__)
class EventPublisher:
    async def publish(self, topic: str, payload: dict) -> None:
        try:
            import nats
            nc = await nats.connect(settings.nats_url)
            await nc.publish(topic, json.dumps(payload, ensure_ascii=False, default=str).encode())
            await nc.drain()
        except Exception as exc:
            logger.warning("event publish skipped", extra={"topic": topic, "error": str(exc)})
