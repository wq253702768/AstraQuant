from jsonschema import Draft202012Validator
from astra_common.errors import AppError
from app.config import settings

SUPPORTED_TIMEFRAMES = {"1m", "5m", "15m", "1h", "4h"}
SUPPORTED_SYMBOLS = {"BTC-USDT-SWAP", "ETH-USDT-SWAP"}
SUPPORTED_DIRECTIONS = {"LONG", "SHORT", "BOTH", "LONG_ONLY", "SHORT_ONLY"}
SUPPORTED_INDICATORS = {"EMA", "SMA", "RSI", "MACD", "ATR", "BOLL", "VOLUME_MA"}

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
                raise AppError("STRATEGY_SYMBOL_INVALID", f"不支持的交易品种：{unsupported}", 422)
        direction = params_json.get("trade_direction") or params_json.get("direction")
        if direction is not None and direction not in SUPPORTED_DIRECTIONS:
            raise AppError("STRATEGY_CONFIG_INVALID", f"trade_direction 仅支持 {sorted(SUPPORTED_DIRECTIONS)}", 422)
        self._validate_indicator_config(params_json.get("indicator_config") or params_json.get("indicators") or {})
        self._validate_entry_rules(params_json.get("entry_rule_config") or params_json.get("entry_rules") or {})
        self._validate_exit_rules(params_json.get("exit_rule_config") or params_json.get("exit_rules") or {})
        max_leverage = params_json.get("max_leverage") or risk_params_json.get("max_leverage")
        if max_leverage is not None and max_leverage > settings.system_max_leverage:
            raise AppError("INVALID_STRATEGY_PARAMS", f"max_leverage 不能超过系统上限 {settings.system_max_leverage}", 422)
        risk_per_trade = params_json.get("risk_per_trade_pct") or risk_params_json.get("max_single_trade_loss_pct")
        if risk_per_trade is not None and risk_per_trade > settings.system_max_risk_per_trade_pct:
            raise AppError("INVALID_STRATEGY_PARAMS", f"单笔风险不能超过 {settings.system_max_risk_per_trade_pct}", 422)
        if params_json.get("funding_rate_filter_enabled", False) and params_json.get("max_abs_funding_rate") is None:
            raise AppError("INVALID_STRATEGY_PARAMS", "启用资金费率过滤时 max_abs_funding_rate 不能为空", 422)

    def _validate_indicator_config(self, config: dict) -> None:
        if not isinstance(config, dict):
            raise AppError("STRATEGY_CONFIG_INVALID", "indicator_config 必须是对象", 422)
        for name, item in config.items():
            if not isinstance(item, dict) or "type" not in item:
                raise AppError("STRATEGY_CONFIG_INVALID", f"指标 {name} 必须包含 type", 422)
            if item["type"] not in SUPPORTED_INDICATORS:
                raise AppError("STRATEGY_CONFIG_INVALID", f"不支持的指标类型 {item['type']}", 422)
            if "period" in item and (not isinstance(item["period"], int) or item["period"] <= 0):
                raise AppError("STRATEGY_CONFIG_INVALID", f"指标 {name}.period 必须是正整数", 422)

    def _validate_entry_rules(self, config: dict) -> None:
        if not config:
            return
        if not isinstance(config, dict):
            raise AppError("STRATEGY_ENTRY_RULE_INVALID", "entry_rule_config 必须是对象", 422)
        if "long" not in config and "short" not in config:
            raise AppError("STRATEGY_ENTRY_RULE_INVALID", "entry_rule_config 至少包含 long 或 short", 422)
        for side in ["long", "short"]:
            if side in config:
                rule = config[side]
                if rule.get("logic", "AND") not in {"AND", "OR"}:
                    raise AppError("STRATEGY_ENTRY_RULE_INVALID", f"{side}.logic 仅支持 AND/OR", 422)
                conditions = rule.get("conditions", [])
                if not isinstance(conditions, list):
                    raise AppError("STRATEGY_ENTRY_RULE_INVALID", f"{side}.conditions 必须是数组", 422)
                for condition in conditions:
                    if not condition.get("operator"):
                        raise AppError("STRATEGY_ENTRY_RULE_INVALID", "开仓条件 operator 不能为空", 422)

    def _validate_exit_rules(self, config: dict) -> None:
        if not config:
            return
        if not isinstance(config, dict):
            raise AppError("STRATEGY_EXIT_RULE_INVALID", "exit_rule_config 必须是对象", 422)
        enabled = [
            config.get("take_profit", {}).get("enabled"),
            config.get("stop_loss", {}).get("enabled"),
            config.get("reverse_signal_exit", {}).get("enabled"),
        ]
        if not any(enabled):
            raise AppError("STRATEGY_EXIT_RULE_INVALID", "平仓规则至少启用止盈、止损或反向信号平仓之一", 422)
