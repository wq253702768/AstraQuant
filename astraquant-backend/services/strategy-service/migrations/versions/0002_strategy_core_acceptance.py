"""strategy core acceptance fields

Revision ID: 0002_strategy_core_acceptance
Revises: 0001_strategy_schema
Create Date: 2026-05-07
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_strategy_core_acceptance"
down_revision = "0001_strategy_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("strategy", sa.Column("latest_version_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("strategy", sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("strategy", sa.Column("archived_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("strategy_template", sa.Column("template_type", sa.String(32), nullable=False, server_default="CONFIG"))
    op.add_column("strategy_template", sa.Column("default_config", postgresql.JSONB, nullable=True))
    op.add_column("strategy_template", sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("strategy_template", sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table(
        "strategy_audit_event_basic",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_username", sa.String(64), nullable=True),
        sa.Column("resource_type", sa.String(64), nullable=True),
        sa.Column("resource_id", sa.String(128), nullable=True),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB, nullable=True),
        sa.Column("ip_address", sa.String(64), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("trace_id", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_strategy_audit_event_type", "strategy_audit_event_basic", ["event_type"])
    op.create_index("idx_strategy_audit_actor", "strategy_audit_event_basic", ["actor_id"])
    op.create_index("idx_strategy_audit_created_at", "strategy_audit_event_basic", ["created_at"])


def downgrade() -> None:
    op.drop_table("strategy_audit_event_basic")
    op.drop_column("strategy_template", "updated_at")
    op.drop_column("strategy_template", "sort_order")
    op.drop_column("strategy_template", "default_config")
    op.drop_column("strategy_template", "template_type")
    op.drop_column("strategy", "archived_at")
    op.drop_column("strategy", "updated_by")
    op.drop_column("strategy", "latest_version_id")
