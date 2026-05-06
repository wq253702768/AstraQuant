from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.reload_strategies_service import ReloadStrategiesService
router=APIRouter(prefix="/signal-runtime", tags=["signal-runtime"])
@router.get("/strategies")
async def strategies(request: Request): return success_response({"items": []}, request)
@router.post("/reload")
async def reload(request: Request): return success_response(await ReloadStrategiesService().execute(), request)
@router.post("/strategies/{strategy_version_id}/pause")
async def pause(strategy_version_id: str, payload: dict, request: Request): return success_response({"strategy_version_id":strategy_version_id,"runtime_status":"PAUSED"}, request)
