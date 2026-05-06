from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class StrategyVersionCreatedEvent:
    event_type: str
    payload: dict
    created_at: datetime
