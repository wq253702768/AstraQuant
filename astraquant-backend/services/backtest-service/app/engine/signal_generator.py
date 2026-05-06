from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class TradeSignal:
    signal_time: datetime
    symbol: str
    signal_type: str
    side: str
    position_side: str
    action: str
    price: Decimal
    size: Decimal | None
    leverage: Decimal
    reason: str
    confidence: float = 1.0
