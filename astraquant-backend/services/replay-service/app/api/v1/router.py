from fastapi import APIRouter
from app.api.v1.endpoints import replay_curves, replay_events, replay_export, replay_klines, replay_page

api_router = APIRouter()
api_router.include_router(replay_page.router)
api_router.include_router(replay_events.router)
api_router.include_router(replay_klines.router)
api_router.include_router(replay_curves.router)
api_router.include_router(replay_export.router)
