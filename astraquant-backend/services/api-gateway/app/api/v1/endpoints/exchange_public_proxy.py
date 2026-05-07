from fastapi import APIRouter, Request

from app.clients.exchange_public_client import ExchangePublicClient
from app.middleware.permissions import require_permission

router = APIRouter(tags=["exchange-public"])


@router.get("/api/exchange-public/health")
async def health(request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", "/health", request)


@router.get("/api/exchange-public/exchanges/{exchange}/time")
async def time(exchange: str, request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", f"/api/v1/exchanges/{exchange}/time", request)


@router.get("/api/exchange-public/exchanges/{exchange}/instruments")
async def instruments(exchange: str, request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", f"/api/v1/exchanges/{exchange}/instruments", request, params=dict(request.query_params))


@router.get("/api/exchange-public/exchanges/{exchange}/ticker")
async def ticker(exchange: str, request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", f"/api/v1/exchanges/{exchange}/ticker", request, params=dict(request.query_params))


@router.get("/api/exchange-public/exchanges/{exchange}/mark-price")
async def mark_price(exchange: str, request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", f"/api/v1/exchanges/{exchange}/mark-price", request, params=dict(request.query_params))


@router.get("/api/exchange-public/exchanges/{exchange}/funding-rate")
async def funding_rate(exchange: str, request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", f"/api/v1/exchanges/{exchange}/funding-rate", request, params=dict(request.query_params))


@router.get("/api/exchange-public/exchanges/{exchange}/klines")
async def klines(exchange: str, request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", f"/api/v1/exchanges/{exchange}/klines", request, params=dict(request.query_params))


@router.get("/api/exchange-public/exchanges/{exchange}/funding-rate-history")
async def funding_rate_history(exchange: str, request: Request):
    require_permission(request, "market_data:read")
    return await ExchangePublicClient().request("GET", f"/api/v1/exchanges/{exchange}/funding-rate-history", request, params=dict(request.query_params))
