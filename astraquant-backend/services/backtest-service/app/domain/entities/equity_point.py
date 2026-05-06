from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class EquityPoint:
    ts: datetime
    equity: Decimal
    cash: Decimal
    position_value: Decimal
    realized_pnl: Decimal
    unrealized_pnl: Decimal
    fee_total: Decimal
    funding_fee_total: Decimal
    drawdown_pct: Decimal = Decimal("0")
