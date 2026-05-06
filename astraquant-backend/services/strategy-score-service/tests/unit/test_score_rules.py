from app.domain.services.admission_rule_engine import AdmissionRuleEngine
from app.scoring.ai_score import AIScore
from app.scoring.cost_score import CostScore
from app.scoring.drawdown_score import DrawdownScore
from app.scoring.profit_score import ProfitScore
from app.scoring.total_score import TotalScore


def test_profit_score_negative_return(): assert ProfitScore().calculate({"total_return": -0.1}) == 0

def test_profit_score_positive(): assert ProfitScore().calculate({"total_return": 0.1, "profit_factor": 1.4}) == 75

def test_drawdown_score_high_risk(): assert DrawdownScore().calculate({"max_drawdown": -0.16}) == 10

def test_cost_score_high_cost(): assert CostScore().calculate({"net_profit": 100, "fee_total": 60, "slippage_total": 0, "funding_fee_total": 0}) == 20

def test_ai_score_missing(): assert AIScore().calculate(None)[0] == 50

def test_ai_score_high_risk(): assert AIScore().calculate({"risk_level": "HIGH"})[0] == 30

def test_total_score_weight(): assert TotalScore().calculate({"profit_score": 100, "drawdown_score": 100, "stability_score": 100, "out_of_sample_score": 100, "cost_score": 100, "risk_score": 100, "ai_score": 100}) == 100

def test_admission_reject_negative_profit(): assert AdmissionRuleEngine().decide({"total_return": -1, "net_profit": -1, "profit_factor": 0}, {}, 0, None, [])[0] == "REJECT"

def test_admission_allow_simulation():
    metrics = {"total_return": 0.2, "net_profit": 1000, "max_drawdown": -0.03, "profit_factor": 1.5}
    assert AdmissionRuleEngine().decide(metrics, {"cost_score": 80}, 85, {"risk_level": "LOW"}, [])[0] == "ALLOW_SIMULATION"

def test_admission_retest_required():
    metrics = {"total_return": 0.2, "net_profit": 1000, "max_drawdown": -0.07, "profit_factor": 1.5}
    assert AdmissionRuleEngine().decide(metrics, {"cost_score": 80}, 85, None, [])[0] == "RETEST_REQUIRED"
