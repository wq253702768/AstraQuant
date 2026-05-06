class LiquidationEstimator:
    def estimate(self, entry_price, leverage, side): return entry_price * (1 - 1 / leverage) if side.upper()=="LONG" else entry_price * (1 + 1 / leverage)
