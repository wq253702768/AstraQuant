from fastapi import APIRouter
from app.api.v1.endpoints import runtime, signals, strategies
api_router=APIRouter(); api_router.include_router(signals.router); api_router.include_router(runtime.router); api_router.include_router(strategies.router)
