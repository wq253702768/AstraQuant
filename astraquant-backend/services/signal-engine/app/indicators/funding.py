from decimal import Decimal
class FundingIndicator:
    def too_high(self, rate: str, max_abs: float) -> bool:
        return abs(Decimal(str(rate or "0"))) > Decimal(str(max_abs))
