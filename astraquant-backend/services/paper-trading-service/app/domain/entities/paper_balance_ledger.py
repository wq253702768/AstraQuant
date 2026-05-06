from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaperBalanceLedger:
    id: str|None
    account_id: str
    ledger_type: str
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    description: str
