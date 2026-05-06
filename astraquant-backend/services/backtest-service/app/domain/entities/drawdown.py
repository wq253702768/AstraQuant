from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class Drawdown:
    drawdown_id: str
    start_time: datetime
    trough_time: datetime
    recovery_time: datetime | None
    peak_equity: Decimal
    trough_equity: Decimal
    drawdown_pct: Decimal
    drawdown_amount: Decimal
    status: str
