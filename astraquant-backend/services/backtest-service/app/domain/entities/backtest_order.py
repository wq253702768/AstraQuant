from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class BacktestOrder:
    order_time: datetime
    symbol: str
    side: str
    position_side: str
    action: str
    order_type: str
    price: Decimal
    size: Decimal
    leverage: Decimal
    cl_ord_id: str
    reason: str
