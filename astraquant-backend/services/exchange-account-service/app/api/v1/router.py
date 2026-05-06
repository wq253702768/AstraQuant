from fastapi import APIRouter
from app.api.v1.endpoints import account_states, connectivity, credentials, exchange_accounts, order_states, position_states
api_router=APIRouter(); api_router.include_router(exchange_accounts.router); api_router.include_router(credentials.router); api_router.include_router(connectivity.router); api_router.include_router(account_states.router); api_router.include_router(position_states.router); api_router.include_router(order_states.router)
