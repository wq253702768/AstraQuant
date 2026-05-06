from typing import Any
import httpx
from fastapi import Request
from fastapi.responses import JSONResponse
from astra_common.response import error_response
from app.config import settings

class AIClient:
    def __init__(self, base_url: str = settings.ai_analysis_service_url): self.base_url = base_url.rstrip("/")
    async def request(self, method: str, path: str, request: Request, json: dict[str, Any] | None = None, params: dict[str, Any] | None = None):
        headers = {"X-Trace-Id": request.state.trace_id, "X-User-Id": request.state.user["id"]}
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.request(method, f"{self.base_url}{path}", json=json, params=params, headers=headers)
        except httpx.HTTPError:
            return JSONResponse(status_code=502, content=error_response("AI_SERVICE_UNAVAILABLE", "AI Analysis Service 暂不可用", request.state.trace_id).model_dump())
        return JSONResponse(status_code=response.status_code, content=response.json())
