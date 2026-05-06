from datetime import datetime

from app.domain.services.timeframe import timeframe_delta

class DataGapDetector:
    def detect(self, existing_times: list[datetime], start_time: datetime, end_time: datetime, timeframe: str) -> list[dict]:
        step = timeframe_delta(timeframe)
        existing = set(existing_times)
        missing_points: list[datetime] = []
        current = start_time
        while current < end_time:
            if current not in existing:
                missing_points.append(current)
            current += step
        return self._merge(missing_points, step)

    def _merge(self, points: list[datetime], step) -> list[dict]:
        if not points:
            return []
        ranges = []
        start = prev = points[0]
        count = 1
        for point in points[1:]:
            if point - prev == step:
                prev = point
                count += 1
                continue
            ranges.append({"start_time": start, "end_time": prev + step, "expected_count": count})
            start = prev = point
            count = 1
        ranges.append({"start_time": start, "end_time": prev + step, "expected_count": count})
        return ranges
