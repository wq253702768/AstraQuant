from fastapi import APIRouter
from app.api.v1.endpoints import strategies, strategy_status, strategy_templates, strategy_versions

api_router = APIRouter()
api_router.include_router(strategy_templates.router)
api_router.include_router(strategies.router)
api_router.include_router(strategy_versions.router)
api_router.include_router(strategy_status.router)
