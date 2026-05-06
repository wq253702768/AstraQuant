from fastapi import APIRouter
from app.api.v1.endpoints import funding_rates, instruments, klines, mark_prices, quality, sync

api_router = APIRouter()
api_router.include_router(sync.router)
api_router.include_router(instruments.router)
api_router.include_router(klines.router)
api_router.include_router(funding_rates.router)
api_router.include_router(mark_prices.router)
api_router.include_router(quality.router)
