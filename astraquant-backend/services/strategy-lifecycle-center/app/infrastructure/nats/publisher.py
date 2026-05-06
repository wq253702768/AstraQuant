from app.infrastructure.nats.topics import AUDIT_EVENT, LIFECYCLE_STATE_CHANGED


class LifecycleEventPublisher:
    def __init__(self) -> None:
        self.published: list[tuple[str, dict]] = []

    async def publish(self, topic: str, payload: dict) -> None:
        self.published.append((topic, payload))

    async def publish_state_changed(self, payload: dict) -> None:
        await self.publish(LIFECYCLE_STATE_CHANGED, payload)

    async def publish_audit(self, payload: dict) -> None:
        await self.publish(AUDIT_EVENT, payload)
