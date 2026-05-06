from decimal import Decimal
from app.config import settings
from app.domain.services.account_summary_builder import AccountSummaryBuilder
from app.domain.services.equity_curve_builder import EquityCurveBuilder
from app.domain.services.live_admission_rule_engine import LiveAdmissionRuleEngine
from app.domain.services.live_report_builder import LiveReportBuilder
from app.domain.services.paper_live_comparator import PaperLiveComparator
from app.domain.services.risk_event_aggregator import RiskEventAggregator
from app.domain.services.strategy_summary_builder import StrategySummaryBuilder


def test_equity_curve_builder(): assert EquityCurveBuilder().point({"starting_equity":"10000","total_equity":"10100"})["drawdown_pct"] == Decimal("0.01")

def test_account_daily_summary_builder(): assert AccountSummaryBuilder().build(Decimal("100"), Decimal("110"), [{"status":"FILLED"}], [{"fee":"1"}])["daily_return"] == Decimal("0.1")

def test_strategy_daily_summary_builder(): assert StrategySummaryBuilder().build()["risk_state"] == "NORMAL"

def test_risk_daily_summary_builder(): assert RiskEventAggregator().aggregate([{"event_type":"order.unknown"}])["order_unknown_count"] == 1

def test_paper_live_comparator(): assert PaperLiveComparator().compare({"total_return":"0.1","max_drawdown":"-0.02","trade_count":10},{"total_return":"0.08","max_drawdown":"-0.03","trade_count":8})["return_deviation"] == Decimal("0.2")

def test_live_admission_continue_small_live():
    m={"observation_days":7,"live_trade_count":10,"total_return":Decimal("0.01"),"max_drawdown":Decimal("-0.025"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.2"),"order_unknown_count":0,"order_failed_count":0,"circuit_breaker_count":0,"emergency_stop_count":0,"cost_to_profit_ratio":Decimal("0.1")}
    assert LiveAdmissionRuleEngine().decide(m, settings)[0] in {"CONTINUE_SMALL_LIVE","ALLOW_SCALE_UP_APPLICATION"}

def test_live_admission_rollback_to_paper():
    m={"total_return":Decimal("-0.02"),"max_drawdown":Decimal("-0.01"),"observation_days":7,"live_trade_count":10}
    assert LiveAdmissionRuleEngine().decide(m, settings)[0] == "ROLLBACK_TO_PAPER"

def test_live_admission_pause_strategy():
    m={"total_return":Decimal("0.01"),"max_drawdown":Decimal("-0.05"),"observation_days":7,"live_trade_count":10}
    assert LiveAdmissionRuleEngine().decide(m, settings)[0] == "PAUSE_STRATEGY"

def test_live_admission_allow_scale_up():
    m={"observation_days":7,"live_trade_count":10,"total_return":Decimal("0.03"),"max_drawdown":Decimal("-0.01"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.3"),"order_unknown_count":0,"order_failed_count":0,"circuit_breaker_count":0,"emergency_stop_count":0,"cost_to_profit_ratio":Decimal("0.1")}
    assert LiveAdmissionRuleEngine().decide(m, settings)[0] == "ALLOW_SCALE_UP_APPLICATION"

def test_live_report_builder(): assert "summary" in LiveReportBuilder().build({})
