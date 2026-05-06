from dataclasses import dataclass

@dataclass(frozen=True)
class RiskDecision:
    decision: str
    reason: str
    triggered_rules: list[str]

class RiskEngine:
    def check(self, signal, risk_model: dict) -> RiskDecision:
        max_leverage = risk_model.get("max_leverage")
        if max_leverage is not None and signal.leverage > max_leverage:
            return RiskDecision("REJECT", "杠杆超过限制", ["max_leverage"])
        return RiskDecision("APPROVE", "风控通过", [])
