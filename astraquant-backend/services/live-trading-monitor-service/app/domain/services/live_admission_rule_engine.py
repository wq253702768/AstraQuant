from decimal import Decimal
class LiveAdmissionRuleEngine:
    def decide(self, metrics: dict, cfg) -> tuple[str,bool,float,list[str],list[str]]:
        if metrics["total_return"] <= Decimal("-0.01"): return "ROLLBACK_TO_PAPER", False, 0, ["实盘收益低于-1%"], []
        if abs(metrics["max_drawdown"]) > cfg.max_live_drawdown_pct: return "PAUSE_STRATEGY", False, 20, ["实盘回撤超过阈值"], []
        if metrics.get("order_unknown_count",0) > 0: return "MANUAL_REVIEW_REQUIRED", False, 40, [], ["存在UNKNOWN订单"]
        if metrics.get("circuit_breaker_count",0) > 1: return "PAUSE_STRATEGY", False, 30, ["熔断次数过多"], []
        if metrics.get("cost_to_profit_ratio",Decimal("0")) > cfg.max_cost_to_profit_ratio: return "EXTEND_OBSERVATION", False, 60, [], ["成本占比偏高"]
        if metrics["observation_days"] >= cfg.min_live_observation_days and metrics["live_trade_count"] >= cfg.min_live_trade_count and metrics["total_return"] > 0 and abs(metrics["max_drawdown"]) <= Decimal("0.02") and metrics["win_rate"] >= Decimal("0.45") and metrics["profit_factor"] >= Decimal("1.2"):
            return "ALLOW_SCALE_UP_APPLICATION", True, 88.5, [], ["允许提交扩大仓位申请，但必须人工审批"]
        return "CONTINUE_SMALL_LIVE", True, 75, [], ["继续小仓实盘观察"]
