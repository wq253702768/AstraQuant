BACKTEST_TRADE_DDL = """
CREATE TABLE IF NOT EXISTS backtest_trade
(
    task_id UUID,
    strategy_id UUID,
    strategy_version_id UUID,
    exchange String,
    internal_symbol String,
    trade_time DateTime64(3),
    side String,
    position_side String,
    action String,
    order_type String,
    order_price Decimal(32,16),
    fill_price Decimal(32,16),
    size Decimal(32,16),
    leverage Decimal(8,2),
    fee Decimal(32,16),
    slippage Decimal(32,16),
    funding_fee Decimal(32,16),
    realized_pnl Decimal(32,16),
    equity_after Decimal(32,16),
    cl_ord_id String,
    reason String,
    created_at DateTime64(3)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(trade_time)
ORDER BY (task_id, internal_symbol, trade_time)
"""

EQUITY_CURVE_DDL = """
CREATE TABLE IF NOT EXISTS strategy_equity_curve
(
    task_id UUID,
    strategy_id UUID,
    strategy_version_id UUID,
    exchange String,
    internal_symbol String,
    ts DateTime64(3),
    equity Decimal(32,16),
    cash Decimal(32,16),
    position_value Decimal(32,16),
    realized_pnl Decimal(32,16),
    unrealized_pnl Decimal(32,16),
    fee_total Decimal(32,16),
    funding_fee_total Decimal(32,16),
    drawdown_pct Decimal(18,8),
    created_at DateTime64(3)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (task_id, ts)
"""

DRAWDOWN_DDL = """
CREATE TABLE IF NOT EXISTS strategy_drawdown
(
    drawdown_id UUID,
    task_id UUID,
    strategy_id UUID,
    strategy_version_id UUID,
    start_time DateTime64(3),
    trough_time DateTime64(3),
    recovery_time Nullable(DateTime64(3)),
    peak_equity Decimal(32,16),
    trough_equity Decimal(32,16),
    drawdown_pct Decimal(18,8),
    drawdown_amount Decimal(32,16),
    trade_count Int32,
    win_rate Decimal(18,8),
    status String,
    main_cause String,
    created_at DateTime64(3)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(start_time)
ORDER BY (task_id, start_time)
"""
