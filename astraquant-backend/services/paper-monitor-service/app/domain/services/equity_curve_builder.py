from decimal import Decimal
class EquityCurveBuilder:
    def point(self, account: dict) -> dict:
        initial = Decimal(str(account.get("initial_balance", "0"))) or Decimal("1")
        equity = Decimal(str(account.get("equity", initial)))
        return {"equity": equity, "total_return": (equity-initial)/initial}
