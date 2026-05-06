from fastapi import APIRouter, Request
from astra_common.response import success_response
from app.application.services.export_replay_service import ExportReplayService

router = APIRouter(prefix="/replays", tags=["replays"])

@router.get("/{drawdown_id}/export")
async def export(drawdown_id: str, request: Request):
    return success_response(await ExportReplayService().execute(drawdown_id), request)
