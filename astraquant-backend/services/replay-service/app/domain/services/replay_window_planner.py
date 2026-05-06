from datetime import datetime, timedelta

class ReplayWindowPlanner:
    def plan(self, start_time: datetime, end_time: datetime, minutes: int = 60) -> list[tuple[datetime, datetime]]:
        windows = []
        current = start_time
        step = timedelta(minutes=minutes)
        while current < end_time:
            nxt = min(current + step, end_time)
            windows.append((current, nxt))
            current = nxt
        return windows
