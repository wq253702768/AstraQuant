from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ReplayWindow:
    start_time: datetime
    end_time: datetime
    limit: int
    cursor: str | None = None
