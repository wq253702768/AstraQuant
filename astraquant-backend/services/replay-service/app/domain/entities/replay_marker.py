from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ReplayMarker:
    marker_type: str
    event_time: datetime
    symbol: str
    payload: dict
