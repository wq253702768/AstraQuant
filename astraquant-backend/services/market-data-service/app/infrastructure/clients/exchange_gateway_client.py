import httpx
from astra_common.errors import AppError
from app.config import settings

class ExchangeGatewayClient:
    def __init__(self, base_url: str = settings.exchange_gateway_url):
        self.base_url = base_url.rstrip("/")

    async def get_instruments(self, exchange: str, contract_type: str = "swap", symbol: str | None = None) -> list[dict]:
        params = {"contract_type": contract_type}
        if symbol: params["symbol"] = symbol
        data = await self._get(f"/api/v1/exchanges/{exchange}/instruments", params)
        return data.get("items", [])

    async def get_klines(self, exchange: str, symbol: str, timeframe: str, start_time: int | None = None, end_time: int | None = None, limit: int = 100) -> list[dict]:
        params = {"symbol": symbol, "timeframe": timeframe, "limit": limit}
        if start_time: params["start_time"] = start_time
        if end_time: params["end_time"] = end_time
        data = await self._get(f"/api/v1/exchanges/{exchange}/klines", params)
        return data.get("items", [])

    async def get_funding_rate_history(self, exchange: str, symbol: str, start_time: int | None = None, end_time: int | None = None, limit: int = 100) -> list[dict]:
        params = {"symbol": symbol, "limit": limit}
        if start_time: params["start_time"] = start_time
        if end_time: params["end_time"] = end_time
        data = await self._get(f"/api/v1/exchanges/{exchange}/funding-rate-history", params)
        return data.get("items", [])

    async def get_mark_price(self, exchange: str, symbol: str) -> dict:
        return await self._get(f"/api/v1/exchanges/{exchange}/mark-price", {"symbol": symbol})

    async def _get(self, path: str, params: dict) -> dict:
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(f"{self.base_url}{path}", params=params)
        except httpx.HTTPError as exc:
            raise AppError("EXCHANGE_GATEWAY_ERROR", str(exc), 502) from exc
        payload = response.json()
        if response.status_code >= 400 or payload.get("code") != "SUCCESS":
            raise AppError("EXCHANGE_GATEWAY_ERROR", payload.get("message", "交易所网关错误"), 502, payload)
        return payload.get("data") or {}
