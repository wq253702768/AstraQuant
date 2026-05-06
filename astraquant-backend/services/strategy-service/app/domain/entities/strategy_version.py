from dataclasses import dataclass
from datetime import datetime

@dataclass
class StrategyVersion:
    id: str
    strategy_id: str
    version: str
    template_id: str
    params_json: dict
    risk_params_json: dict
    params_hash: str
    status: str
    created_by: str
    code_hash: str | None = None
    source_version_id: str | None = None
    created_source: str = "manual"
    created_at: datetime | None = None
