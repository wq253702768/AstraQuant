from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperStrategyDailySummary:
    strategy_version_id: str
    trade_count: int
    daily_return: Decimal
