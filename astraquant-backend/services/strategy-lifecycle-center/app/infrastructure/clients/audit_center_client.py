from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class AuditCenterClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.audit_center_service_url)
