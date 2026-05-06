from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperAccount:
    id: str|None
    name: str
    exchange: str
    currency: str
    initial_balance: Decimal
    available_balance: Decimal
    margin_used: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    equity: Decimal
    status: str
