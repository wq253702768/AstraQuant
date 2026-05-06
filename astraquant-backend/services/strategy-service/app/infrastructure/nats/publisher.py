import json
import logging
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

class EventPublisher:
    async def publish(self, topic: str, payload: dict[str, Any]) -> None:
        try:
            import nats
            nc = await nats.connect(settings.nats_url)
            await nc.publish(topic, json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8"))
            await nc.drain()
        except Exception as exc:  # Sprint 2 allows running without local NATS in unit tests.
            logger.warning("event publish skipped", extra={"topic": topic, "error": str(exc)})
