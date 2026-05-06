from app.config import settings
from app.infrastructure.clients.service_client import ServiceClient


class AiAnalysisServiceClient(ServiceClient):
    def __init__(self) -> None:
        super().__init__(settings.ai_analysis_service_url)
