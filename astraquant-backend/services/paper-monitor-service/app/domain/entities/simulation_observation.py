from dataclasses import dataclass
from decimal import Decimal

@dataclass
class SimulationObservation:
    id: str|None
    account_id: str
    strategy_id: str
    strategy_version_id: str
    status: str
