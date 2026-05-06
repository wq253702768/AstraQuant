from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperOrder:
    id: str|None
    account_id: str
    signal_id: str
    risk_decision_id: str
    strategy_id: str
    strategy_version_id: str
    exchange: str
    internal_symbol: str
    side: str
    position_side: str
    action: str
    order_type: str
    requested_price: Decimal|None
    quantity: Decimal
    leverage: Decimal
    status: str
    idempotency_key: str
