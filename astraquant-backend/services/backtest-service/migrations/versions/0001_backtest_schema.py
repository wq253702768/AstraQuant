"""create backtest schema

Revision ID: 0001_backtest_schema
Revises:
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_backtest_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("backtest_task", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("exchange", sa.String(32), nullable=False), sa.Column("symbols", postgresql.JSONB, nullable=False), sa.Column("timeframe", sa.String(16), nullable=False), sa.Column("start_time", sa.DateTime(timezone=True), nullable=False), sa.Column("end_time", sa.DateTime(timezone=True), nullable=False), sa.Column("initial_capital", sa.Numeric(32, 8), nullable=False), sa.Column("cost_model", postgresql.JSONB, nullable=False), sa.Column("risk_model", postgresql.JSONB, nullable=False), sa.Column("data_snapshot_id", postgresql.UUID(as_uuid=True)), sa.Column("params_hash", sa.String(128)), sa.Column("code_hash", sa.String(128)), sa.Column("status", sa.String(64), nullable=False), sa.Column("progress", sa.Numeric(5, 2), nullable=False, server_default="0"), sa.Column("current_stage", sa.String(64)), sa.Column("processed_bars", sa.Integer(), server_default="0"), sa.Column("total_bars", sa.Integer(), server_default="0"), sa.Column("error_message", sa.Text()), sa.Column("created_by", postgresql.UUID(as_uuid=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_backtest_task_strategy_version", "backtest_task", ["strategy_version_id"])
    op.create_index("idx_backtest_task_status", "backtest_task", ["status"])
    op.create_index("idx_backtest_task_created_at", "backtest_task", ["created_at"])
    op.create_index("idx_backtest_task_exchange", "backtest_task", ["exchange"])
    op.create_table("backtest_result", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("backtest_task.id"), nullable=False), sa.Column("total_return", sa.Numeric(18, 8)), sa.Column("annual_return", sa.Numeric(18, 8)), sa.Column("final_equity", sa.Numeric(32, 8)), sa.Column("max_drawdown", sa.Numeric(18, 8)), sa.Column("max_drawdown_amount", sa.Numeric(32, 8)), sa.Column("win_rate", sa.Numeric(18, 8)), sa.Column("profit_loss_ratio", sa.Numeric(18, 8)), sa.Column("profit_factor", sa.Numeric(18, 8)), sa.Column("trade_count", sa.Integer()), sa.Column("win_trade_count", sa.Integer()), sa.Column("loss_trade_count", sa.Integer()), sa.Column("max_consecutive_losses", sa.Integer()), sa.Column("avg_profit", sa.Numeric(32, 8)), sa.Column("avg_loss", sa.Numeric(32, 8)), sa.Column("fee_total", sa.Numeric(32, 8)), sa.Column("slippage_total", sa.Numeric(32, 8)), sa.Column("funding_fee_total", sa.Numeric(32, 8)), sa.Column("gross_profit", sa.Numeric(32, 8)), sa.Column("gross_loss", sa.Numeric(32, 8)), sa.Column("net_profit", sa.Numeric(32, 8)), sa.Column("score", sa.Numeric(8, 2)), sa.Column("decision", sa.String(64)), sa.Column("summary_json", postgresql.JSONB), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("uk_backtest_result_task", "backtest_result", ["task_id"], unique=True)

def downgrade() -> None:
    op.drop_table("backtest_result")
    op.drop_table("backtest_task")
