from dataclasses import dataclass

@dataclass(frozen=True)
class StrategyTemplate:
    id: str
    code: str
    name: str
    strategy_type: str
    default_params: dict
    param_schema: dict
    risk_schema: dict
    description: str | None
    enabled: bool
