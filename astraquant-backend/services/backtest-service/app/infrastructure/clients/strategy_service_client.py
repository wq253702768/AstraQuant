import httpx
from app.config import settings

class StrategyServiceClient:
    async def get_version(self, strategy_version_id: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{settings.strategy_service_url}/strategy-versions/{strategy_version_id}")
        if response.status_code >= 400:
            return {}
        payload = response.json()
        return payload.get("data") or {}
