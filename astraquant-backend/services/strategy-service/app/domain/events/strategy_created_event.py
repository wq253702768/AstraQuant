from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class StrategyCreatedEvent:
    event_type: str
    payload: dict
    created_at: datetime
