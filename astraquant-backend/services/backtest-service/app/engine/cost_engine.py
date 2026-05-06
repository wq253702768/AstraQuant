from decimal import Decimal

class CostEngine:
    def fee(self, price: Decimal, size: Decimal, fee_rate: Decimal) -> Decimal:
        return abs(price * size * fee_rate)
    def apply_slippage(self, price: Decimal, side: str, slippage: Decimal) -> tuple[Decimal, Decimal]:
        signed = price * slippage
        if side.lower() == "buy":
            return price + signed, signed
        return price - signed, signed
    def funding_fee(self, notional: Decimal, funding_rate: Decimal) -> Decimal:
        return notional * funding_rate
