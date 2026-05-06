from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperStrategyPerformance:
    strategy_version_id: str
    total_return: Decimal
    trade_count: int
