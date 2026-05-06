from fastapi import APIRouter
from app.api.v1.endpoints import backtests, drawdowns, metrics, trades

api_router = APIRouter()
api_router.include_router(backtests.router)
api_router.include_router(trades.router)
api_router.include_router(drawdowns.router)
api_router.include_router(metrics.router)
