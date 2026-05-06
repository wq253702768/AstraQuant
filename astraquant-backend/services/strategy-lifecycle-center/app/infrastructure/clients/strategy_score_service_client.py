from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class StrategyScoreServiceClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.strategy_score_service_url)
