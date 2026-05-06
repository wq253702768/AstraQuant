from decimal import Decimal
class SimulationAdmissionRuleEngine:
    def decide(self, metrics: dict, cfg) -> tuple[str,bool,float,list[str],list[str],list[dict]]:
        reasons=[]; warnings=[]; suggestions=[]
        if metrics["observation_days"] < cfg.min_observation_days: return "CONTINUE_OBSERVATION", False, 0, [], ["观察天数不足"], []
        if metrics["trade_count"] < cfg.min_trade_count: return "CONTINUE_OBSERVATION", False, 0, [], ["交易次数不足"], []
        if metrics["total_return"] <= 0: return "REJECT_SMALL_LIVE", False, 0, ["收益为负"], [], []
        if abs(metrics["max_drawdown"]) > Decimal("0.08"): return "REJECT_SMALL_LIVE", False, 20, ["最大回撤过大"], [], []
        if metrics.get("order_error_count",0) > cfg.max_order_error_count: return "MANUAL_REVIEW_REQUIRED", False, 40, [], ["存在订单异常"], []
        if metrics.get("cost_to_profit_ratio",Decimal("0")) > cfg.max_cost_to_profit_ratio: return "RETEST_REQUIRED", False, 60, [], ["成本占比过高"], []
        passed = abs(metrics["max_drawdown"]) <= cfg.max_drawdown_pct and metrics["win_rate"] >= Decimal("0.45") and metrics["profit_factor"] >= Decimal("1.2") and metrics["max_consecutive_losses"] <= cfg.max_consecutive_losses
        if passed:
            return "ALLOW_SMALL_LIVE_APPLICATION", True, 86.5, [], ["仍需人工审批后才可进入小仓实盘"], [{"type":"APPLY_SMALL_LIVE","content":"允许提交小仓实盘申请，建议初始仓位不超过账户权益的5%"}]
        return "RETEST_REQUIRED", False, 65, [], ["模拟盘表现未完全达标"], [{"type":"RETEST","content":"建议优化后重新回测"}]
