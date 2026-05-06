from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_replay_curves_service import QueryReplayCurvesService

router = APIRouter(prefix="/replays", tags=["replays"])

@router.get("/{drawdown_id}/curves")
async def curves(drawdown_id: str, request: Request):
    return success_response(await QueryReplayCurvesService().execute(drawdown_id), request)
