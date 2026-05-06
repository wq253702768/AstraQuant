from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(frozen=True)
class BacktestTrade:
    trade_time: datetime
    symbol: str
    side: str
    position_side: str
    action: str
    order_type: str
    order_price: Decimal
    fill_price: Decimal
    size: Decimal
    leverage: Decimal
    fee: Decimal
    slippage: Decimal
    funding_fee: Decimal
    realized_pnl: Decimal
    equity_after: Decimal
    cl_ord_id: str
    reason: str
