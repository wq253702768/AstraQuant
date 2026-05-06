class FundingEngine:
    def funding_fee(self, notional, funding_rate, position_side):
        fee = notional * funding_rate
        return fee if position_side.upper() == "LONG" else -fee
