from typing import Any

import httpx


class ServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    async def get(self, path: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(f"{self.base_url}{path}")
            response.raise_for_status()
            payload = response.json()
            return payload.get("data", payload) if isinstance(payload, dict) else {"payload": payload}
