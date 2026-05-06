from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class StrategyStatusLog:
    id: str
    strategy_id: str
    strategy_version_id: str | None
    from_status: str | None
    to_status: str
    reason: str | None
    operator_id: str
    created_at: datetime | None = None
