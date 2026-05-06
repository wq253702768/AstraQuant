from datetime import datetime
from decimal import Decimal

from app.domain.enums.quality_status import QualityStatus
from app.domain.services.data_gap_detector import DataGapDetector
from app.domain.services.timeframe import timeframe_delta

class DataQualityChecker:
    def check_klines(self, rows: list[dict], exchange: str, symbol: str, timeframe: str, start_time: datetime, end_time: datetime) -> dict:
        step = timeframe_delta(timeframe)
        expected_count = max(0, int((end_time - start_time) / step))
        times = [row["ts"] for row in rows]
        missing_ranges = DataGapDetector().detect(times, start_time, end_time, timeframe)
        missing_count = sum(item["expected_count"] for item in missing_ranges)
        duplicate_count = len(times) - len(set(times))
        warning_items = []
        abnormal_count = 0
        for row in rows:
            o, h, l, c = (Decimal(str(row[key])) for key in ("open", "high", "low", "close"))
            if o <= 0 or h <= 0 or l <= 0 or c <= 0:
                abnormal_count += 1
                warning_items.append({"type": "non_positive_price", "ts": row["ts"].isoformat()})
            elif h < o or h < c or l > o or l > c:
                abnormal_count += 1
                warning_items.append({"type": "invalid_ohlc", "ts": row["ts"].isoformat()})
        missing_rate = (missing_count / expected_count) if expected_count else 0
        status = QualityStatus.PASS
        if abnormal_count > 0 or duplicate_count > 0 or 0 < missing_rate <= 0.005:
            status = QualityStatus.WARNING
        if missing_rate > 0.005 or any(item["type"] == "non_positive_price" for item in warning_items):
            status = QualityStatus.FAILED
        return {"exchange": exchange, "internal_symbol": symbol, "data_type": "kline", "timeframe": timeframe, "start_time": start_time, "end_time": end_time, "status": status.value, "expected_count": expected_count, "actual_count": len(rows), "missing_count": missing_count, "duplicate_count": duplicate_count, "abnormal_count": abnormal_count, "missing_ranges": missing_ranges, "warning_items": warning_items, "detail_json": {}}
