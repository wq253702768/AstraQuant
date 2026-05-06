from dataclasses import dataclass
@dataclass
class StrategyRuntime:
    strategy_id: str
    strategy_version_id: str
    exchange: str
    internal_symbol: str
    runtime_status: str
