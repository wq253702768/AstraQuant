from dataclasses import dataclass
@dataclass
class IndicatorState:
    strategy_version_id: str
    symbol: str
    values: dict
