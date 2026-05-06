import pytest
from astra_common.errors import AppError
from app.agents.data_validator_agent import DataValidatorAgent
from app.agents.opponent_reviewer_agent import OpponentReviewerAgent
from app.agents.parameter_optimizer_agent import ParameterOptimizerAgent
from app.domain.enums.ai_task_status import AITaskStatus
from app.domain.services.ai_output_validator import AIOutputValidator
from app.domain.services.ai_task_state_machine import AITaskStateMachine
from app.domain.services.input_data_hash_service import InputDataHashService
from app.domain.services.prompt_render_service import PromptRenderService
from app.graph.backtest_review_graph import BacktestReviewGraph


def test_input_data_hash_stable():
    service = InputDataHashService()
    assert service.calculate({"b": 2, "a": 1}) == service.calculate({"a": 1, "b": 2})


def test_ai_output_validator_success():
    AIOutputValidator().validate({"agent_name": "x", "conclusion": "ok", "evidence": ["a"], "risk_level": "LOW", "suggestions": [], "confidence": 0.5})


def test_ai_output_validator_failed():
    with pytest.raises(AppError):
        AIOutputValidator().validate({"agent_name": "x"})


def test_parameter_suggestion_need_retest():
    with pytest.raises(AppError):
        AIOutputValidator().validate({"agent_name": "x", "conclusion": "ok", "evidence": ["a"], "risk_level": "LOW", "suggestions": [{"type": "PARAMETER_CHANGE", "need_retest": False}], "confidence": 0.5})


def test_prompt_render_service():
    assert PromptRenderService().render("hello {{name}}", {"name": "AI"}) == "hello AI"


def test_ai_task_state_transition():
    AITaskStateMachine().ensure(AITaskStatus.CREATED.value, AITaskStatus.QUEUED.value)
    with pytest.raises(AppError):
        AITaskStateMachine().ensure(AITaskStatus.CREATED.value, AITaskStatus.COMPLETED.value)


def test_data_validator_agent_mock():
    output = DataValidatorAgent().run({})
    assert output["can_continue"] is True
    AIOutputValidator().validate(output)


def test_opponent_reviewer_detects_missing_evidence():
    output = OpponentReviewerAgent().run({})
    assert output["detected_issues"][0]["issue_type"] == "OUT_OF_SAMPLE_MISSING"


def test_parameter_optimizer_need_retest():
    output = ParameterOptimizerAgent().run({})
    assert output["suggestions"][0]["need_retest"] is True


def test_backtest_review_graph():
    state = BacktestReviewGraph().invoke({"input_data": {}, "errors": []})
    assert state["summary_output"]["final_recommendation"] == "RETEST_REQUIRED"
