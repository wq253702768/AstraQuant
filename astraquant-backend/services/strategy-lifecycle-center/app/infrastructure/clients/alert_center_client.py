from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class AlertCenterClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.alert_center_service_url)

