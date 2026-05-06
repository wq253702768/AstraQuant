from fastapi import APIRouter
from app.api.v1.endpoints import accounts, ledger, orders, performance, positions, trades
api_router=APIRouter(); api_router.include_router(accounts.router); api_router.include_router(positions.router); api_router.include_router(orders.router); api_router.include_router(trades.router); api_router.include_router(ledger.router); api_router.include_router(performance.router)
