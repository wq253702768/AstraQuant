from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ReplayEvent:
    task_id: str
    drawdown_id: str
    event_time: datetime
    event_type: str
    marker_type: str | None
    exchange: str
    internal_symbol: str
    strategy_id: str
    strategy_version_id: str
    sequence_no: int
    payload: dict
