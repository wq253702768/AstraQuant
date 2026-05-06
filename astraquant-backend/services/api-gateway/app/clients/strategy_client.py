from typing import Any

import httpx
from fastapi import Request

from astra_common.errors import AppError
from app.config import settings


class StrategyClient:
    def __init__(self, base_url: str = settings.strategy_service_url):
        self.base_url = base_url.rstrip("/")

    async def request(
        self,
        method: str,
        path: str,
        request: Request,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict:
        headers = {
            "X-Trace-Id": request.state.trace_id,
            "X-User-Id": request.state.user["id"],
        }
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.request(
                    method,
                    f"{self.base_url}{path}",
                    json=json,
                    params=params,
                    headers=headers,
                )
        except httpx.RequestError as exc:
            raise AppError("STRATEGY_SERVICE_UNAVAILABLE", "Strategy Service 暂不可用", 502) from exc
        return response.json()
