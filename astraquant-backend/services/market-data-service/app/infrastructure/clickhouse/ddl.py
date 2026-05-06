MARKET_KLINE_DDL = """
CREATE TABLE IF NOT EXISTS market_kline
(
    exchange String,
    internal_symbol String,
    exchange_symbol String,
    timeframe String,
    ts DateTime64(3),
    open Decimal(32,16),
    high Decimal(32,16),
    low Decimal(32,16),
    close Decimal(32,16),
    volume Decimal(32,16),
    quote_volume Decimal(32,16),
    created_at DateTime64(3)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (exchange, internal_symbol, timeframe, ts)
"""

FUNDING_RATE_DDL = """
CREATE TABLE IF NOT EXISTS funding_rate_history
(
    exchange String,
    internal_symbol String,
    exchange_symbol String,
    funding_rate Decimal(18,10),
    realized_rate Decimal(18,10),
    funding_time DateTime64(3),
    next_funding_time DateTime64(3),
    mark_price Decimal(32,16),
    created_at DateTime64(3)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(funding_time)
ORDER BY (exchange, internal_symbol, funding_time)
"""

MARK_PRICE_DDL = """
CREATE TABLE IF NOT EXISTS mark_price_history
(
    exchange String,
    internal_symbol String,
    exchange_symbol String,
    mark_price Decimal(32,16),
    index_price Decimal(32,16),
    ts DateTime64(3),
    created_at DateTime64(3)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (exchange, internal_symbol, ts)
"""
