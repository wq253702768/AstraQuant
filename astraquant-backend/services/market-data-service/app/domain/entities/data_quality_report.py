from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class MissingRange:
    start_time: datetime
    end_time: datetime
    expected_count: int

@dataclass(frozen=True)
class DataQualityReport:
    exchange: str
    internal_symbol: str
    data_type: str
    timeframe: str | None
    start_time: datetime
    end_time: datetime
    status: str
    expected_count: int
    actual_count: int
    missing_count: int
    duplicate_count: int
    abnormal_count: int
    missing_ranges: list[dict]
    warning_items: list[dict]
