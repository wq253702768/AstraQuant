from jsonschema import Draft202012Validator
from astra_common.errors import AppError
from app.config import settings

SUPPORTED_TIMEFRAMES = {"1m", "5m", "15m", "1h"}
SUPPORTED_SYMBOLS = {"BTC-USDT-SWAP", "ETH-USDT-SWAP"}

class StrategyParamValidator:
    def validate(self, params_json: dict, risk_params_json: dict, param_schema: dict, risk_schema: dict) -> None:
        self._validate_json_schema(params_json, param_schema, "INVALID_STRATEGY_PARAMS")
        self._validate_json_schema(risk_params_json, risk_schema, "INVALID_RISK_PARAMS")
        self._validate_common_rules(params_json, risk_params_json)

    def _validate_json_schema(self, payload: dict, schema: dict, code: str) -> None:
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
        if errors:
            first = errors[0]
            path = ".".join(str(item) for item in first.path) or "root"
            raise AppError(code, f"{path}: {first.message}", 422, {"field": path, "reason": first.message})

    def _validate_common_rules(self, params_json: dict, risk_params_json: dict) -> None:
        timeframe = params_json.get("timeframe")
        if timeframe is not None and timeframe not in SUPPORTED_TIMEFRAMES:
            raise AppError("INVALID_STRATEGY_PARAMS", f"timeframe 仅支持 {sorted(SUPPORTED_TIMEFRAMES)}", 422)
        symbols = params_json.get("symbols")
        if symbols is not None:
            if not symbols:
                raise AppError("INVALID_STRATEGY_PARAMS", "symbols 不能为空", 422)
            unsupported = [symbol for symbol in symbols if symbol not in SUPPORTED_SYMBOLS]
            if unsupported:
                raise AppError("INVALID_STRATEGY_PARAMS", f"不支持的交易品种：{unsupported}", 422)
        max_leverage = params_json.get("max_leverage") or risk_params_json.get("max_leverage")
        if max_leverage is not None and max_leverage > settings.system_max_leverage:
            raise AppError("INVALID_STRATEGY_PARAMS", f"max_leverage 不能超过系统上限 {settings.system_max_leverage}", 422)
        risk_per_trade = params_json.get("risk_per_trade_pct") or risk_params_json.get("max_single_trade_loss_pct")
        if risk_per_trade is not None and risk_per_trade > settings.system_max_risk_per_trade_pct:
            raise AppError("INVALID_STRATEGY_PARAMS", f"单笔风险不能超过 {settings.system_max_risk_per_trade_pct}", 422)
        if params_json.get("funding_rate_filter_enabled", False) and params_json.get("max_abs_funding_rate") is None:
            raise AppError("INVALID_STRATEGY_PARAMS", "启用资金费率过滤时 max_abs_funding_rate 不能为空", 422)
