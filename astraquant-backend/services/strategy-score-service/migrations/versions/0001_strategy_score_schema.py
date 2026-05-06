"""create strategy score schema

Revision ID: 0001_strategy_score_schema
Revises:
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = "0001_strategy_score_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("strategy_score", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("backtest_task_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("ai_task_id", postgresql.UUID(as_uuid=True)), sa.Column("total_score", sa.Numeric(8,2), nullable=False), sa.Column("grade", sa.String(8), nullable=False), sa.Column("profit_score", sa.Numeric(8,2), nullable=False), sa.Column("drawdown_score", sa.Numeric(8,2), nullable=False), sa.Column("stability_score", sa.Numeric(8,2), nullable=False), sa.Column("out_of_sample_score", sa.Numeric(8,2), nullable=False), sa.Column("cost_score", sa.Numeric(8,2), nullable=False), sa.Column("risk_score", sa.Numeric(8,2), nullable=False), sa.Column("ai_score", sa.Numeric(8,2), nullable=False), sa.Column("decision", sa.String(64), nullable=False), sa.Column("reject_reasons", postgresql.JSONB), sa.Column("warnings", postgresql.JSONB), sa.Column("suggestions", postgresql.JSONB), sa.Column("detail_json", postgresql.JSONB, nullable=False), sa.Column("created_by", postgresql.UUID(as_uuid=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_strategy_score_strategy_version", "strategy_score", ["strategy_version_id"])
    op.create_index("idx_strategy_score_backtest_task", "strategy_score", ["backtest_task_id"])
    op.create_index("idx_strategy_score_ai_task", "strategy_score", ["ai_task_id"])
    op.create_index("idx_strategy_score_decision", "strategy_score", ["decision"])
    op.create_index("idx_strategy_score_created_at", "strategy_score", ["created_at"])
def downgrade() -> None:
    op.drop_table("strategy_score")
