class TotalScore:
    weights = {"profit_score": 0.20, "drawdown_score": 0.25, "stability_score": 0.15, "out_of_sample_score": 0.10, "cost_score": 0.10, "risk_score": 0.10, "ai_score": 0.10}
    def calculate(self, scores: dict) -> float:
        return round(sum(scores[key] * weight for key, weight in self.weights.items()), 2)
    def grade(self, total: float) -> str:
        if total >= 90: return "A"
        if total >= 80: return "B"
        if total >= 70: return "C"
        if total >= 60: return "D"
        return "E"
