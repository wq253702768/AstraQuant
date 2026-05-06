import httpx
from fastapi import Request
from app.config import settings

class AuthClient:
    def __init__(self, base_url: str = settings.auth_service_url):
        self.base_url = base_url.rstrip("/")

    async def login(self, payload: dict, request: Request) -> dict:
        return await self._post("/auth/login", payload, request)

    async def refresh(self, payload: dict, request: Request) -> dict:
        return await self._post("/auth/refresh", payload, request)

    async def logout(self, payload: dict, request: Request) -> dict:
        return await self._request("POST", "/auth/logout", payload, request, include_auth=True)

    async def change_password(self, payload: dict, request: Request) -> dict:
        return await self._request("PUT", "/auth/password", payload, request, include_auth=True)

    async def me(self, token: str, request: Request) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{self.base_url}/auth/me", headers={"Authorization": f"Bearer {token}", "X-Trace-Id": request.state.trace_id})
        return response.json()

    async def _post(self, path: str, payload: dict, request: Request) -> dict:
        return await self._request("POST", path, payload, request)

    async def _request(self, method: str, path: str, payload: dict, request: Request, include_auth: bool = False) -> dict:
        headers = {"X-Trace-Id": request.state.trace_id}
        if include_auth:
            headers["Authorization"] = request.headers.get("Authorization", "")
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.request(method, f"{self.base_url}{path}", json=payload, headers=headers)
        return response.json()
