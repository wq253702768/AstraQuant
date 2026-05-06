from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class BacktestResult:
    task_id: str
    total_return: Decimal
    final_equity: Decimal
    max_drawdown: Decimal
    win_rate: Decimal
    trade_count: int
    net_profit: Decimal
