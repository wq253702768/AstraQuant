from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperEquityCurve:
    account_id: str
    equity: Decimal
