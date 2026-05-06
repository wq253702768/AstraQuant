from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperRiskEventSummary:
    strategy_version_id: str
    risk_reject_count: int
