from datetime import datetime, timedelta

class SyncWindowPlanner:
    kline_windows = {"1m": timedelta(days=3), "5m": timedelta(days=15), "15m": timedelta(days=30), "1h": timedelta(days=90)}
    funding_window = timedelta(days=90)

    def plan_kline_windows(self, start_time: datetime, end_time: datetime, timeframe: str) -> list[tuple[datetime, datetime]]:
        return self._split(start_time, end_time, self.kline_windows.get(timeframe, timedelta(days=7)))

    def plan_funding_windows(self, start_time: datetime, end_time: datetime) -> list[tuple[datetime, datetime]]:
        return self._split(start_time, end_time, self.funding_window)

    def _split(self, start_time: datetime, end_time: datetime, step: timedelta) -> list[tuple[datetime, datetime]]:
        windows = []
        current = start_time
        while current < end_time:
            nxt = min(current + step, end_time)
            windows.append((current, nxt))
            current = nxt
        return windows
