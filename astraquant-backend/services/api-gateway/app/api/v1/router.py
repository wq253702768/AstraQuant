from fastapi import APIRouter
from app.api.v1.endpoints import auth_proxy, dashboard, realtime_ws, task_ws

api_router = APIRouter()
api_router.include_router(auth_proxy.router)
api_router.include_router(dashboard.router)
api_router.include_router(task_ws.router)
api_router.include_router(realtime_ws.router)
