from app.domain.enums.admission_decision import AdmissionDecision

class AdmissionRuleEngine:
    def decide(self, metrics: dict, scores: dict, total_score: float, ai_result: dict | None, warnings: list[str]) -> tuple[str, list[str], list[str]]:
        reject_reasons = []
        if metrics.get("total_return", 0) <= 0: reject_reasons.append("总收益率小于等于0")
        if metrics.get("net_profit", 0) <= 0: reject_reasons.append("净利润小于等于0")
        if abs(metrics.get("max_drawdown", 0)) > 0.15: reject_reasons.append("最大回撤超过15%")
        if metrics.get("profit_factor", 0) < 1.0: reject_reasons.append("Profit Factor 小于1")
        if ai_result and ai_result.get("risk_level") == "CRITICAL": reject_reasons.append("AI反方审查为CRITICAL")
        if reject_reasons: return AdmissionDecision.REJECT.value, reject_reasons, warnings
        if warnings or scores.get("cost_score", 100) < 60 or abs(metrics.get("max_drawdown", 0)) >= 0.06:
            return AdmissionDecision.RETEST_REQUIRED.value, [], warnings
        if total_score >= 90:
            return AdmissionDecision.ALLOW_SMALL_LIVE_AFTER_SIMULATION.value, [], warnings
        if total_score >= 80 and abs(metrics.get("max_drawdown", 0)) <= 0.08 and metrics.get("profit_factor", 0) >= 1.3:
            return AdmissionDecision.ALLOW_SIMULATION.value, [], warnings
        return AdmissionDecision.RETEST_REQUIRED.value, [], warnings
