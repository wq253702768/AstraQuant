from datetime import datetime
from fastapi import APIRouter, Query, Request
from astra_common.response import success_response
from app.application.services.query_replay_events_service import QueryReplayEventsService

router = APIRouter(prefix="/replays", tags=["replays"])

@router.get("/{drawdown_id}/events")
async def events(drawdown_id: str, request: Request, start_time: datetime | None = None, end_time: datetime | None = None, event_type: str | None = None, marker_type: str | None = None, cursor: str | None = None, limit: int = Query(500, ge=1, le=2000)):
    return success_response(await QueryReplayEventsService().execute(drawdown_id, start_time, end_time, event_type, marker_type, cursor, limit), request)
