from fastapi import APIRouter, Request
from app.clients.market_data_client import MarketDataClient
from app.middleware.permissions import require_permission

router = APIRouter(tags=["market-data"])

@router.post("/api/market-data/sync")
async def create_sync(payload: dict, request: Request):
    require_permission(request, "market_data:sync")
    return await MarketDataClient().request("POST", "/market-data/sync", request, payload)

@router.get("/api/market-data/sync/{sync_task_id}")
async def get_sync(sync_task_id: str, request: Request):
    require_permission(request, "market_data:read")
    return await MarketDataClient().request("GET", f"/market-data/sync/{sync_task_id}", request)

@router.get("/api/market-data/instruments")
async def instruments(request: Request):
    require_permission(request, "market_data:read")
    return await MarketDataClient().request("GET", "/market-data/instruments", request, params=dict(request.query_params))

@router.get("/api/market-data/klines")
async def klines(request: Request):
    require_permission(request, "market_data:read")
    return await MarketDataClient().request("GET", "/market-data/klines", request, params=dict(request.query_params))

@router.get("/api/market-data/funding-rates")
async def funding_rates(request: Request):
    require_permission(request, "market_data:read")
    return await MarketDataClient().request("GET", "/market-data/funding-rates", request, params=dict(request.query_params))

@router.get("/api/market-data/mark-prices")
async def mark_prices(request: Request):
    require_permission(request, "market_data:read")
    return await MarketDataClient().request("GET", "/market-data/mark-prices", request, params=dict(request.query_params))

@router.get("/api/market-data/quality")
async def quality(request: Request):
    require_permission(request, "market_data:read")
    return await MarketDataClient().request("GET", "/market-data/quality", request, params=dict(request.query_params))
