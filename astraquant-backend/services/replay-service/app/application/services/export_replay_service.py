from datetime import UTC, datetime

class ExportReplayService:
    async def execute(self, drawdown_id: str):
        return {"drawdown_id": drawdown_id, "events": [], "export_time": datetime.now(UTC).isoformat()}
