"""create replay schema

Revision ID: 0001_replay_schema
Revises:
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_replay_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("replay_build_task", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("backtest_task_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("status", sa.String(64), nullable=False), sa.Column("progress", sa.Numeric(5, 2), nullable=False, server_default="0"), sa.Column("current_stage", sa.String(64)), sa.Column("error_message", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_replay_build_task_backtest", "replay_build_task", ["backtest_task_id"])
    op.create_index("idx_replay_build_task_status", "replay_build_task", ["status"])

def downgrade() -> None:
    op.drop_table("replay_build_task")
