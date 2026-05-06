class CostScore:
    def calculate(self, metrics: dict) -> float:
        net = metrics.get("net_profit", 0)
        if net <= 0: return 0
        cost = abs(metrics.get("fee_total", 0) + metrics.get("slippage_total", 0) + metrics.get("funding_fee_total", 0))
        ratio = cost / abs(net) if net else 999
        if ratio > 0.5: return 20
        if ratio >= 0.3: return 40
        if ratio >= 0.2: return 60
        if ratio >= 0.1: return 80
        return 90
