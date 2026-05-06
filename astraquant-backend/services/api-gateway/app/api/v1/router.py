from fastapi import APIRouter
from app.api.v1.endpoints import ai_proxy, auth_proxy, backtest_proxy, dashboard, market_data_proxy, realtime_ws, replay_proxy, report_proxy, strategy_proxy, strategy_score_proxy, task_ws

api_router = APIRouter()
api_router.include_router(auth_proxy.router)
api_router.include_router(dashboard.router)
api_router.include_router(strategy_proxy.router)
api_router.include_router(market_data_proxy.router)
api_router.include_router(backtest_proxy.router)
api_router.include_router(replay_proxy.router)
api_router.include_router(ai_proxy.router)
api_router.include_router(strategy_score_proxy.router)
api_router.include_router(report_proxy.router)
api_router.include_router(task_ws.router)
api_router.include_router(realtime_ws.router)
