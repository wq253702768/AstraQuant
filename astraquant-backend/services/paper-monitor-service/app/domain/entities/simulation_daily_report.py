from dataclasses import dataclass
from decimal import Decimal

@dataclass
class SimulationDailyReport:
    report_date: str
    report_json: dict
