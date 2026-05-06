from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class LiveMonitorServiceClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.live_monitor_service_url)
