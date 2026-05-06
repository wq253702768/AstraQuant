from app.domain.entities.paper_balance_ledger import PaperBalanceLedger
class LedgerEngine:
    def entry(self, account_id, ledger_type, amount, before, after, description): return PaperBalanceLedger(None, account_id, ledger_type, amount, before, after, description)
