from fastapi import APIRouter
from app.api.v1.endpoints import decisions, scores
api_router = APIRouter()
api_router.include_router(scores.router)
api_router.include_router(decisions.router)
