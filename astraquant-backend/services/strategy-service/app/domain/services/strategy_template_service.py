from copy import deepcopy

DEFAULT_RISK_PARAMS = {
    "max_single_trade_loss_pct": 0.005,
    "max_daily_loss_pct": 0.02,
    "max_strategy_drawdown_pct": 0.06,
    "max_account_drawdown_pct": 0.10,
    "max_consecutive_losses": 3,
    "max_leverage": 3,
    "max_position_pct": 0.2,
    "liquidation_distance_min_pct": 0.10,
    "market_data_stale_seconds": 3,
    "order_unknown_block_enabled": True,
    "position_inconsistent_block_enabled": True,
}

RISK_SCHEMA = {
    "type": "object",
    "required": ["max_single_trade_loss_pct", "max_daily_loss_pct", "max_strategy_drawdown_pct", "max_consecutive_losses"],
    "properties": {
        "max_single_trade_loss_pct": {"type": "number", "exclusiveMinimum": 0, "maximum": 0.02},
        "max_daily_loss_pct": {"type": "number", "exclusiveMinimum": 0, "maximum": 0.2},
        "max_strategy_drawdown_pct": {"type": "number", "exclusiveMinimum": 0, "maximum": 0.5},
        "max_account_drawdown_pct": {"type": "number", "exclusiveMinimum": 0, "maximum": 0.5},
        "max_consecutive_losses": {"type": "integer", "minimum": 1},
        "max_leverage": {"type": "number", "minimum": 1, "maximum": 10},
        "max_position_pct": {"type": "number", "exclusiveMinimum": 0, "maximum": 1},
        "liquidation_distance_min_pct": {"type": "number", "exclusiveMinimum": 0},
        "market_data_stale_seconds": {"type": "integer", "minimum": 1},
        "order_unknown_block_enabled": {"type": "boolean"},
        "position_inconsistent_block_enabled": {"type": "boolean"},
    },
    "additionalProperties": True,
}

COMMON_PROPERTIES = {
    "exchange": {"type": "string", "enum": ["OKX"]},
    "symbols": {"type": "array", "items": {"type": "string", "enum": ["BTC-USDT-SWAP", "ETH-USDT-SWAP"]}, "minItems": 1},
    "timeframe": {"type": "string", "enum": ["1m", "5m", "15m", "1h"]},
    "direction": {"type": "string", "enum": ["LONG", "SHORT", "BOTH"]},
    "max_leverage": {"type": "number", "minimum": 1, "maximum": 10},
    "risk_per_trade_pct": {"type": "number", "exclusiveMinimum": 0, "maximum": 0.02},
    "max_abs_funding_rate": {"type": ["number", "null"]},
}

def strategy_templates() -> list[dict]:
    return [
        {
            "code": "trend_breakout",
            "name": "趋势突破策略",
            "strategy_type": "trend_breakout",
            "description": "突破关键高点/低点后顺势交易",
            "default_params": {
                "exchange": "OKX", "symbols": ["BTC-USDT-SWAP"], "timeframe": "5m", "direction": "BOTH",
                "breakout_window": 288, "breakout_confirm_minutes": 3, "volume_confirm_enabled": True,
                "volume_multiplier": 1.5, "max_leverage": 3, "position_sizing_mode": "risk_based",
                "risk_per_trade_pct": 0.005, "stop_loss_pct": 0.006, "take_profit_mode": "partial",
                "take_profit_r_multiple": 2, "trailing_stop_enabled": True,
                "funding_rate_filter_enabled": True, "max_abs_funding_rate": 0.0005,
            },
            "param_schema": {
                "type": "object",
                "required": ["exchange", "symbols", "timeframe", "direction", "breakout_window", "breakout_confirm_minutes", "max_leverage", "risk_per_trade_pct", "stop_loss_pct"],
                "properties": {**COMMON_PROPERTIES, "breakout_window": {"type": "integer", "minimum": 1}, "breakout_confirm_minutes": {"type": "integer", "minimum": 1}, "stop_loss_pct": {"type": "number", "exclusiveMinimum": 0}, "funding_rate_filter_enabled": {"type": "boolean"}},
                "additionalProperties": True,
            },
        },
        {
            "code": "pullback_follow",
            "name": "回调跟随策略",
            "strategy_type": "pullback_follow",
            "description": "趋势中回踩支撑后入场",
            "default_params": {"exchange": "OKX", "symbols": ["BTC-USDT-SWAP"], "timeframe": "5m", "direction": "BOTH", "trend_ma_period": 120, "pullback_ma_period": 20, "atr_period": 14, "pullback_atr_multiplier": 1.2, "max_leverage": 3, "risk_per_trade_pct": 0.005, "stop_loss_atr_multiplier": 1.5, "take_profit_r_multiple": 2.0, "funding_rate_filter_enabled": True, "max_abs_funding_rate": 0.0005},
            "param_schema": {"type": "object", "required": ["exchange", "symbols", "timeframe", "direction", "trend_ma_period", "pullback_ma_period", "max_leverage", "risk_per_trade_pct"], "properties": {**COMMON_PROPERTIES, "trend_ma_period": {"type": "integer", "minimum": 1}, "pullback_ma_period": {"type": "integer", "minimum": 1}}, "additionalProperties": True},
        },
        {
            "code": "grid_strategy",
            "name": "网格震荡策略",
            "strategy_type": "grid_strategy",
            "description": "横盘区间低买高卖",
            "default_params": {"exchange": "OKX", "symbols": ["BTC-USDT-SWAP"], "timeframe": "5m", "grid_mode": "neutral", "upper_price": None, "lower_price": None, "grid_count": 10, "single_grid_position_pct": 0.02, "max_total_position_pct": 0.2, "max_leverage": 2, "post_only_enabled": True, "rebalance_interval_seconds": 30, "min_reprice_interval_seconds": 15, "funding_rate_filter_enabled": True, "max_abs_funding_rate": 0.0005},
            "param_schema": {"type": "object", "required": ["exchange", "symbols", "timeframe", "grid_count", "single_grid_position_pct", "max_total_position_pct", "max_leverage"], "properties": {**COMMON_PROPERTIES, "grid_count": {"type": "integer", "minimum": 2, "maximum": 100}, "single_grid_position_pct": {"type": "number", "exclusiveMinimum": 0}, "max_total_position_pct": {"type": "number", "exclusiveMinimum": 0, "maximum": 1}}, "additionalProperties": True},
        },
        {
            "code": "defense_strategy",
            "name": "空仓防御策略",
            "strategy_type": "defense_strategy",
            "description": "高波动、插针、数据异常时不交易",
            "default_params": {"exchange": "OKX", "symbols": ["BTC-USDT-SWAP", "ETH-USDT-SWAP"], "volatility_window": 60, "max_volatility_pct": 0.03, "max_spread_pct": 0.001, "max_abs_funding_rate": 0.0008, "min_orderbook_depth_usdt": 100000, "stale_market_data_seconds": 3, "pause_minutes_after_trigger": 30},
            "param_schema": {"type": "object", "required": ["exchange", "symbols", "volatility_window", "max_volatility_pct", "max_spread_pct", "max_abs_funding_rate", "stale_market_data_seconds"], "properties": {"exchange": COMMON_PROPERTIES["exchange"], "symbols": COMMON_PROPERTIES["symbols"], "volatility_window": {"type": "integer", "minimum": 1}, "max_volatility_pct": {"type": "number", "exclusiveMinimum": 0}, "max_spread_pct": {"type": "number", "exclusiveMinimum": 0}, "max_abs_funding_rate": {"type": "number"}, "stale_market_data_seconds": {"type": "integer", "minimum": 1}}, "additionalProperties": True},
        },
    ]

def template_seed_rows() -> list[dict]:
    rows = []
    for template in strategy_templates():
        row = deepcopy(template)
        row["risk_schema"] = deepcopy(RISK_SCHEMA)
        row["enabled"] = True
        rows.append(row)
    return rows
