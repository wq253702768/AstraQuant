class ReplayEventRepository:
    def __init__(self, client=None): self.client = client; self.memory: list[dict] = []
    def batch_insert(self, events: list) -> None:
        rows = [event.__dict__ | {"payload_json": event.payload} for event in events]
        if self.client and rows: self.client.insert("replay_event", rows)
        self.memory.extend(rows)
    def query(self, drawdown_id: str, start_time=None, end_time=None, event_type=None, marker_type=None, limit: int = 500):
        rows = [row for row in self.memory if row["drawdown_id"] == drawdown_id]
        if start_time: rows = [row for row in rows if row["event_time"] >= start_time]
        if end_time: rows = [row for row in rows if row["event_time"] <= end_time]
        if event_type: rows = [row for row in rows if row["event_type"] == event_type]
        if marker_type: rows = [row for row in rows if row["marker_type"] == marker_type]
        return sorted(rows, key=lambda row: (row["event_time"], row["sequence_no"]))[:limit]
