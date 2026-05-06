from dataclasses import dataclass
from datetime import datetime

@dataclass
class SyncTask:
    id: str
    exchange: str
    symbols: list[str]
    data_types: list[str]
    timeframes: list[str] | None
    start_time: datetime | None
    end_time: datetime | None
    force_resync: bool
    status: str
    progress: float
