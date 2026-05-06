class RiskScore:
    def calculate(self, metrics: dict) -> float:
        if metrics.get("max_leverage", 1) > 5: return 30
        if metrics.get("max_consecutive_losses", 0) > 6: return 40
        if abs(metrics.get("max_drawdown", 0)) > metrics.get("max_drawdown_threshold", 0.15): return 40
        return 80
