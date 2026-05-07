import pytest
from astra_common.errors import AppError
from app.domain.enums.strategy_status import StrategyStatus
from app.domain.services.strategy_param_validator import StrategyParamValidator
from app.domain.services.strategy_state_machine import StrategyStateMachine
from app.domain.services.strategy_template_service import DEFAULT_RISK_PARAMS, template_seed_rows
from app.schemas.strategy import CopyStrategyRequest, CreateStrategyRequest, UpdateStrategyRequest
from app.utils.hash_utils import calc_params_hash


def test_calc_params_hash_stable():
    left = calc_params_hash({"b": 2, "a": 1}, {"risk": True})
    right = calc_params_hash({"a": 1, "b": 2}, {"risk": True})
    assert left == right


def test_state_transition_valid():
    machine = StrategyStateMachine()
    assert machine.can_transition(StrategyStatus.DRAFT.value, StrategyStatus.READY_FOR_BACKTEST.value)


def test_state_transition_invalid():
    machine = StrategyStateMachine()
    with pytest.raises(AppError):
        machine.ensure_transition(StrategyStatus.DRAFT.value, StrategyStatus.BACKTESTING.value)


def test_param_validator_success():
    template = next(item for item in template_seed_rows() if item["code"] == "trend_breakout")
    StrategyParamValidator().validate(template["default_params"], DEFAULT_RISK_PARAMS, template["param_schema"], template["risk_schema"])


def test_param_validator_missing_required():
    template = next(item for item in template_seed_rows() if item["code"] == "trend_breakout")
    params = dict(template["default_params"])
    params.pop("exchange")
    with pytest.raises(AppError):
        StrategyParamValidator().validate(params, DEFAULT_RISK_PARAMS, template["param_schema"], template["risk_schema"])


def test_strategy_create_request_allows_optional_template_and_list_tags():
    payload = CreateStrategyRequest(name="BTC 趋势", code="btc_trend", strategy_type="CONFIG", tags=["BTC", "趋势"])
    assert payload.template_id is None
    assert payload.tags == ["BTC", "趋势"]


def test_strategy_update_and_copy_payloads():
    update = UpdateStrategyRequest(name="新名称", tags=["EMA"])
    copy = CopyStrategyRequest(name="副本", code="copy_code")
    assert update.tags == ["EMA"]
    assert copy.code == "copy_code"
