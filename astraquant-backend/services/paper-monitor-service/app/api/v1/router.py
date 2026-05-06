from fastapi import APIRouter
from app.api.v1.endpoints import admission, daily_reports, dashboard, equity, observations, risk_events, strategy_summary
api_router=APIRouter(); api_router.include_router(observations.router); api_router.include_router(admission.router); api_router.include_router(dashboard.router); api_router.include_router(equity.router); api_router.include_router(strategy_summary.router); api_router.include_router(daily_reports.router); api_router.include_router(risk_events.router)
