from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Position:
    symbol: str
    position_side: str
    quantity: Decimal = Decimal("0")
    entry_price: Decimal = Decimal("0")
    leverage: Decimal = Decimal("1")
    realized_pnl: Decimal = Decimal("0")
    unrealized_pnl: Decimal = Decimal("0")
