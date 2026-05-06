from typing import Any
import httpx
from fastapi import Request
from fastapi.responses import JSONResponse
from astra_common.response import error_response
from app.config import settings
class RealtimeStateClient:
    def __init__(self, base_url: str = settings.realtime_state_service_url): self.base_url=base_url.rstrip("/")
    async def request(self, method: str, path: str, request: Request, params: dict[str, Any] | None = None):
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response=await client.request(method, f"{self.base_url}{path}", params=params, headers={"X-Trace-Id":request.state.trace_id})
        except httpx.HTTPError:
            return JSONResponse(status_code=502, content=error_response("REALTIME_STATE_SERVICE_UNAVAILABLE", "Realtime State Service 暂不可用", request.state.trace_id).model_dump())
        return JSONResponse(status_code=response.status_code, content=response.json())
