from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class OrderExecutorServiceClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.order_executor_service_url)
