from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class StrategyScore:
    strategy_version_id: str
    backtest_task_id: str
    total_score: Decimal
    grade: str
    decision: str
