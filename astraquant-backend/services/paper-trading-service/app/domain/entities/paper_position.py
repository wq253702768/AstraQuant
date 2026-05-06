from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperPosition:
    id: str|None
    account_id: str
    strategy_id: str
    strategy_version_id: str
    exchange: str
    internal_symbol: str
    position_side: str
    quantity: Decimal
    entry_price: Decimal
    mark_price: Decimal
    leverage: Decimal
    margin: Decimal
    unrealized_pnl: Decimal
    realized_pnl: Decimal
    status: str
