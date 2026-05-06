from decimal import Decimal
from app.domain.entities.paper_account import PaperAccount
class AccountEngine:
    def create(self, name: str, exchange: str, currency: str, initial_balance: Decimal, created_by: str|None=None) -> PaperAccount:
        return PaperAccount(None,name,exchange,currency,initial_balance,initial_balance,Decimal("0"),Decimal("0"),Decimal("0"),initial_balance,"ACTIVE")
    def apply_open(self, account: PaperAccount, margin: Decimal, fee: Decimal) -> PaperAccount:
        account.available_balance -= margin + fee; account.margin_used += margin; account.equity = account.available_balance + account.margin_used + account.unrealized_pnl; return account
    def apply_close(self, account: PaperAccount, released_margin: Decimal, realized_pnl: Decimal, fee: Decimal) -> PaperAccount:
        account.available_balance += released_margin + realized_pnl - fee; account.margin_used -= released_margin; account.realized_pnl += realized_pnl - fee; account.equity = account.available_balance + account.margin_used + account.unrealized_pnl; return account
