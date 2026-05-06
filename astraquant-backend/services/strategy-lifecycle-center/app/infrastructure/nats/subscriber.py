from app.application.services.lifecycle_service import LifecycleApplicationService


class LifecycleSubscriber:
    def __init__(self, service: LifecycleApplicationService | None = None) -> None:
        self.service = service or LifecycleApplicationService()

    async def handle(self, topic: str, payload: dict) -> dict:
        return self.service.consume_event(topic, payload)
