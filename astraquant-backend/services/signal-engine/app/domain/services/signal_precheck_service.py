from decimal import Decimal
from app.config import settings
from app.domain.entities.signal_precheck import SignalPrecheck

class SignalPrecheckService:
    def check(self, snapshot: dict, params: dict, opening: bool = True) -> SignalPrecheck:
        freshness = snapshot.get("freshness") or {"fresh": snapshot.get("fresh", True), "freshness_status": snapshot.get("freshness_status", "FRESH")}
        if opening and not freshness.get("fresh", True):
            return SignalPrecheck(False, "行情数据过期，禁止生成开仓信号", freshness)
        bbo = snapshot.get("bbo") or {}
        spread_pct = Decimal(str(bbo.get("spread_pct", "0") or "0"))
        if opening and spread_pct > Decimal(str(params.get("max_spread_pct", settings.max_spread_pct))):
            return SignalPrecheck(False, "盘口价差过大，禁止生成开仓信号", freshness)
        funding = snapshot.get("funding") or {}
        funding_rate = Decimal(str(funding.get("funding_rate", "0") or "0"))
        if opening and abs(funding_rate) > Decimal(str(params.get("max_abs_funding_rate", settings.max_abs_funding_rate))):
            return SignalPrecheck(False, "资金费率过高，禁止生成开仓信号", freshness)
        return SignalPrecheck(True, "前置校验通过", freshness)
