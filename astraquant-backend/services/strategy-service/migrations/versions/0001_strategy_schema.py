"""create strategy schema

Revision ID: 0001_strategy_schema
Revises:
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_strategy_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("strategy_template", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("code", sa.String(128), nullable=False, unique=True), sa.Column("name", sa.String(128), nullable=False), sa.Column("strategy_type", sa.String(64), nullable=False), sa.Column("default_params", postgresql.JSONB, nullable=False), sa.Column("param_schema", postgresql.JSONB, nullable=False), sa.Column("risk_schema", postgresql.JSONB, nullable=False), sa.Column("description", sa.Text()), sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("idx_strategy_template_type", "strategy_template", ["strategy_type"])
    op.create_index("idx_strategy_template_enabled", "strategy_template", ["enabled"])
    op.create_table("strategy", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("name", sa.String(128), nullable=False), sa.Column("code", sa.String(128), nullable=False, unique=True), sa.Column("strategy_type", sa.String(64), nullable=False), sa.Column("description", sa.Text()), sa.Column("status", sa.String(64), nullable=False), sa.Column("tags", postgresql.JSONB), sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("deleted_at", sa.DateTime(timezone=True)))
    op.create_index("idx_strategy_status", "strategy", ["status"])
    op.create_index("idx_strategy_type", "strategy", ["strategy_type"])
    op.create_table("strategy_version", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategy.id"), nullable=False), sa.Column("version", sa.String(32), nullable=False), sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategy_template.id"), nullable=False), sa.Column("params_json", postgresql.JSONB, nullable=False), sa.Column("risk_params_json", postgresql.JSONB, nullable=False), sa.Column("params_hash", sa.String(128), nullable=False), sa.Column("code_hash", sa.String(128)), sa.Column("source_version_id", postgresql.UUID(as_uuid=True)), sa.Column("created_source", sa.String(64), nullable=False, server_default="manual"), sa.Column("status", sa.String(64), nullable=False, server_default="draft"), sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_unique_constraint("uk_strategy_version", "strategy_version", ["strategy_id", "version"])
    op.create_index("idx_strategy_version_strategy", "strategy_version", ["strategy_id"])
    op.create_index("idx_strategy_version_status", "strategy_version", ["status"])
    op.create_table("strategy_status_log", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("strategy_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategy.id"), nullable=False), sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("strategy_version.id")), sa.Column("from_status", sa.String(64)), sa.Column("to_status", sa.String(64), nullable=False), sa.Column("reason", sa.Text()), sa.Column("operator_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("idx_strategy_status_log_strategy", "strategy_status_log", ["strategy_id"])
    op.create_index("idx_strategy_status_log_created_at", "strategy_status_log", ["created_at"])

def downgrade() -> None:
    op.drop_table("strategy_status_log")
    op.drop_table("strategy_version")
    op.drop_table("strategy")
    op.drop_table("strategy_template")
