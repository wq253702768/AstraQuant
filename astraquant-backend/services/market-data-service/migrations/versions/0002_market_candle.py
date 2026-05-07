"""market candle table

Revision ID: 0002_market_candle
Revises: 0001_market_data_schema
Create Date: 2026-05-07
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_market_candle"
down_revision = "0001_market_data_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "market_candle",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("exchange", sa.String(32), nullable=False),
        sa.Column("internal_symbol", sa.String(64), nullable=False),
        sa.Column("timeframe", sa.String(16), nullable=False),
        sa.Column("open_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("close_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open", sa.Numeric(32, 16), nullable=False),
        sa.Column("high", sa.Numeric(32, 16), nullable=False),
        sa.Column("low", sa.Numeric(32, 16), nullable=False),
        sa.Column("close", sa.Numeric(32, 16), nullable=False),
        sa.Column("volume", sa.Numeric(32, 16)),
        sa.Column("volume_ccy", sa.Numeric(32, 16)),
        sa.Column("volume_ccy_quote", sa.Numeric(32, 16)),
        sa.Column("confirm", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("source", sa.String(64), nullable=False),
        sa.Column("sync_job_id", postgresql.UUID(as_uuid=True)),
        sa.Column("raw_json", postgresql.JSONB),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_unique_constraint("uk_market_candle", "market_candle", ["exchange", "internal_symbol", "timeframe", "open_time"])
    op.create_index("idx_market_candle_symbol_time", "market_candle", ["internal_symbol", "timeframe", "open_time"])
    op.create_index("idx_market_candle_exchange_symbol_time", "market_candle", ["exchange", "internal_symbol", "timeframe", "open_time"])
    op.create_index("idx_market_candle_confirm", "market_candle", ["confirm"])


def downgrade() -> None:
    op.drop_table("market_candle")
