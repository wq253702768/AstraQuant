from dataclasses import dataclass
from decimal import Decimal

@dataclass
class SimulationAdmissionResult:
    decision: str
    passed: bool
    score: Decimal
