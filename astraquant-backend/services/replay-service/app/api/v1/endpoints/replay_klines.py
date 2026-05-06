from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.query_replay_klines_service import QueryReplayKlinesService

router = APIRouter(prefix="/replays", tags=["replays"])

@router.get("/{drawdown_id}/klines")
async def klines(drawdown_id: str, request: Request):
    return success_response(await QueryReplayKlinesService().execute(drawdown_id), request)
