class StabilityScore:
    def calculate(self, metrics: dict) -> float:
        if metrics.get("trade_count", 0) < 30: return 30
        losses = metrics.get("max_consecutive_losses", 0)
        if losses > 8: return 30
        if losses >= 5: return 55
        if losses >= 3: return 75
        return 90
