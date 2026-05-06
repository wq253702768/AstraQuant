REPLAY_EVENT_DDL = """
CREATE TABLE IF NOT EXISTS replay_event
(
    task_id UUID,
    drawdown_id UUID,
    event_time DateTime64(3),
    event_type String,
    marker_type String,
    exchange String,
    internal_symbol String,
    strategy_id UUID,
    strategy_version_id UUID,
    sequence_no UInt64,
    payload_json String,
    created_at DateTime64(3)
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (task_id, drawdown_id, event_time, sequence_no)
"""
