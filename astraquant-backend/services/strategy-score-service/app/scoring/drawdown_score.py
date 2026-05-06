class DrawdownScore:
    def calculate(self, metrics: dict) -> float:
        dd = abs(metrics.get("max_drawdown", 0))
        if dd > 0.15: return 10
        if dd >= 0.10: return 30
        if dd >= 0.08: return 50
        if dd >= 0.06: return 65
        if dd >= 0.04: return 80
        if dd >= 0.02: return 90
        return 95
