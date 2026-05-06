from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperTrade:
    id: str|None
    account_id: str
    paper_order_id: str
    fill_price: Decimal
    quantity: Decimal
    notional_value: Decimal
    fee: Decimal
    slippage: Decimal
    funding_fee: Decimal
    realized_pnl: Decimal
    equity_after: Decimal
