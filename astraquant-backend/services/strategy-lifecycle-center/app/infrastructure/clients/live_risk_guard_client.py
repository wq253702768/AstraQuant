from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class LiveRiskGuardClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.live_risk_guard_service_url)
