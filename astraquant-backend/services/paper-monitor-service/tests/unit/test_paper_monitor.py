from decimal import Decimal
from app.config import settings
from app.domain.services.admission_explanation_builder import AdmissionExplanationBuilder
from app.domain.services.daily_report_builder import DailyReportBuilder
from app.domain.services.daily_summary_builder import DailySummaryBuilder
from app.domain.services.equity_curve_builder import EquityCurveBuilder
from app.domain.services.risk_event_aggregator import RiskEventAggregator
from app.domain.services.simulation_admission_rule_engine import SimulationAdmissionRuleEngine


def test_equity_curve_builder(): assert EquityCurveBuilder().point({"initial_balance":"10000","equity":"10100"})["total_return"] == Decimal("0.01")

def test_daily_summary_builder():
    s=DailySummaryBuilder().build([{"realized_pnl":"10","fee":"1"},{"realized_pnl":"-5","fee":"1"}], Decimal("100"), Decimal("110"))
    assert s["trade_count"] == 2 and s["win_rate"] == Decimal("0.5")

def test_risk_event_aggregator(): assert RiskEventAggregator().aggregate([{"decision":"REJECT"},{"decision":"APPROVE"}])["risk_reject_count"] == 1

def test_admission_reject_negative_return():
    m={"observation_days":7,"trade_count":20,"total_return":Decimal("-0.01"),"max_drawdown":Decimal("-0.01"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.3"),"max_consecutive_losses":2,"cost_to_profit_ratio":Decimal("0.1")}
    assert SimulationAdmissionRuleEngine().decide(m, settings)[0] == "REJECT_SMALL_LIVE"

def test_admission_continue_observation_days_not_enough():
    m={"observation_days":3,"trade_count":20,"total_return":Decimal("0.01"),"max_drawdown":Decimal("-0.01"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.3"),"max_consecutive_losses":2,"cost_to_profit_ratio":Decimal("0.1")}
    assert SimulationAdmissionRuleEngine().decide(m, settings)[0] == "CONTINUE_OBSERVATION"

def test_admission_continue_trade_count_not_enough():
    m={"observation_days":7,"trade_count":3,"total_return":Decimal("0.01"),"max_drawdown":Decimal("-0.01"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.3"),"max_consecutive_losses":2,"cost_to_profit_ratio":Decimal("0.1")}
    assert SimulationAdmissionRuleEngine().decide(m, settings)[0] == "CONTINUE_OBSERVATION"

def test_admission_reject_high_drawdown():
    m={"observation_days":7,"trade_count":20,"total_return":Decimal("0.01"),"max_drawdown":Decimal("-0.09"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.3"),"max_consecutive_losses":2,"cost_to_profit_ratio":Decimal("0.1")}
    assert SimulationAdmissionRuleEngine().decide(m, settings)[0] == "REJECT_SMALL_LIVE"

def test_admission_retest_high_cost():
    m={"observation_days":7,"trade_count":20,"total_return":Decimal("0.01"),"max_drawdown":Decimal("-0.02"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.3"),"max_consecutive_losses":2,"cost_to_profit_ratio":Decimal("0.5")}
    assert SimulationAdmissionRuleEngine().decide(m, settings)[0] == "RETEST_REQUIRED"

def test_admission_allow_small_live_application():
    m={"observation_days":7,"trade_count":20,"total_return":Decimal("0.04"),"max_drawdown":Decimal("-0.02"),"win_rate":Decimal("0.5"),"profit_factor":Decimal("1.3"),"max_consecutive_losses":2,"cost_to_profit_ratio":Decimal("0.1")}
    assert SimulationAdmissionRuleEngine().decide(m, settings)[0] == "ALLOW_SMALL_LIVE_APPLICATION"

def test_admission_explanation_builder(): assert AdmissionExplanationBuilder().build("x", [], ["w"], [])["warnings"] == ["w"]

def test_daily_report_builder(): assert "summary" in DailyReportBuilder().build({})
