class ProfitScore:
    def calculate(self, metrics: dict) -> float:
        if metrics.get("total_return", 0) <= 0: return 0
        pf = metrics.get("profit_factor", 0)
        if pf < 1.1: return 40
        if pf < 1.3: return 60
        if pf < 1.6: return 75
        if pf < 2.0: return 85
        return 95
