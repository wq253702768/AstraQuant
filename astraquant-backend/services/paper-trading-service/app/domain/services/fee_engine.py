from decimal import Decimal
class FeeEngine:
    def fee(self, notional: Decimal, rate: Decimal) -> Decimal: return abs(notional * rate)
