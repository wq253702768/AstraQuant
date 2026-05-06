from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class PaperMonitorServiceClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.paper_monitor_service_url)
