from app.domain.services.cursor_paginator import CursorPaginator

class QueryReplayEventsService:
    def __init__(self, repository=None): self.repository = repository
    async def execute(self, drawdown_id: str, start_time=None, end_time=None, event_type=None, marker_type=None, cursor=None, limit: int = 500):
        rows = self.repository.query(drawdown_id, start_time, end_time, event_type, marker_type, 2000) if self.repository else []
        items, next_cursor = CursorPaginator().page(rows, min(limit, 2000), cursor)
        return {"events": items, "next_cursor": next_cursor}
