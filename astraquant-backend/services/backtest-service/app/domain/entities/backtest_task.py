from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class BacktestTask:
    id: str
    strategy_id: str
    strategy_version_id: str
    exchange: str
    symbols: list[str]
    timeframe: str
    start_time: datetime
    end_time: datetime
    initial_capital: Decimal
    cost_model: dict
    risk_model: dict
    status: str
