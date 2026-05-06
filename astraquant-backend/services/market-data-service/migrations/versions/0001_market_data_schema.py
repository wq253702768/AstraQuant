"""create market data schema

Revision ID: 0001_market_data_schema
Revises:
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_market_data_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("market_data_sync_task", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("exchange", sa.String(32), nullable=False), sa.Column("symbols", postgresql.JSONB, nullable=False), sa.Column("data_types", postgresql.JSONB, nullable=False), sa.Column("timeframes", postgresql.JSONB), sa.Column("start_time", sa.DateTime(timezone=True)), sa.Column("end_time", sa.DateTime(timezone=True)), sa.Column("force_resync", sa.Boolean(), nullable=False, server_default=sa.text("false")), sa.Column("status", sa.String(64), nullable=False), sa.Column("progress", sa.Numeric(5, 2), nullable=False, server_default="0"), sa.Column("current_stage", sa.String(64)), sa.Column("error_message", sa.Text()), sa.Column("created_by", postgresql.UUID(as_uuid=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_market_data_sync_task_status", "market_data_sync_task", ["status"])
    op.create_index("idx_market_data_sync_task_exchange", "market_data_sync_task", ["exchange"])
    op.create_index("idx_market_data_sync_task_created_at", "market_data_sync_task", ["created_at"])
    op.create_table("instrument_config", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("exchange", sa.String(32), nullable=False), sa.Column("internal_symbol", sa.String(64), nullable=False), sa.Column("exchange_symbol", sa.String(64), nullable=False), sa.Column("base_asset", sa.String(32)), sa.Column("quote_asset", sa.String(32)), sa.Column("margin_asset", sa.String(32)), sa.Column("contract_type", sa.String(32), nullable=False), sa.Column("tick_size", sa.Numeric(32, 16)), sa.Column("lot_size", sa.Numeric(32, 16)), sa.Column("min_size", sa.Numeric(32, 16)), sa.Column("contract_value", sa.Numeric(32, 16)), sa.Column("price_precision", sa.Integer()), sa.Column("size_precision", sa.Integer()), sa.Column("status", sa.String(32), nullable=False), sa.Column("raw_json", postgresql.JSONB), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("uk_instrument_config_symbol", "instrument_config", ["exchange", "internal_symbol"], unique=True)
    op.create_index("idx_instrument_config_exchange", "instrument_config", ["exchange"])
    op.create_index("idx_instrument_config_status", "instrument_config", ["status"])
    op.create_table("data_quality_report", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("exchange", sa.String(32), nullable=False), sa.Column("internal_symbol", sa.String(64), nullable=False), sa.Column("data_type", sa.String(64), nullable=False), sa.Column("timeframe", sa.String(16)), sa.Column("start_time", sa.DateTime(timezone=True), nullable=False), sa.Column("end_time", sa.DateTime(timezone=True), nullable=False), sa.Column("status", sa.String(32), nullable=False), sa.Column("expected_count", sa.Integer()), sa.Column("actual_count", sa.Integer()), sa.Column("missing_count", sa.Integer()), sa.Column("duplicate_count", sa.Integer()), sa.Column("abnormal_count", sa.Integer()), sa.Column("missing_ranges", postgresql.JSONB), sa.Column("warning_items", postgresql.JSONB), sa.Column("detail_json", postgresql.JSONB), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_data_quality_symbol", "data_quality_report", ["exchange", "internal_symbol"])
    op.create_index("idx_data_quality_status", "data_quality_report", ["status"])
    op.create_index("idx_data_quality_time", "data_quality_report", ["start_time", "end_time"])

def downgrade() -> None:
    op.drop_table("data_quality_report")
    op.drop_table("instrument_config")
    op.drop_table("market_data_sync_task")
