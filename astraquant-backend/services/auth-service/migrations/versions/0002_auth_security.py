"""add auth security tables

Revision ID: 0002_auth_security
Revises: 0001_auth_schema
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_auth_security"
down_revision = "0001_auth_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "refresh_token",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user_account.id"), nullable=False),
        sa.Column("token_hash", sa.String(256), nullable=False),
        sa.Column("issued_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True)),
        sa.Column("user_agent", sa.Text()),
        sa.Column("ip_address", sa.String(64)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("uk_refresh_token_hash", "refresh_token", ["token_hash"], unique=True)
    op.create_index("idx_refresh_token_user", "refresh_token", ["user_id"])
    op.create_index("idx_refresh_token_expires", "refresh_token", ["expires_at"])

    op.create_table(
        "audit_event_basic",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True)),
        sa.Column("actor_username", sa.String(64)),
        sa.Column("resource_type", sa.String(64)),
        sa.Column("resource_id", sa.String(128)),
        sa.Column("action", sa.String(128), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB),
        sa.Column("ip_address", sa.String(64)),
        sa.Column("user_agent", sa.Text()),
        sa.Column("trace_id", sa.String(128)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("idx_audit_basic_event_type", "audit_event_basic", ["event_type"])
    op.create_index("idx_audit_basic_actor", "audit_event_basic", ["actor_id"])
    op.create_index("idx_audit_basic_created_at", "audit_event_basic", ["created_at"])


def downgrade() -> None:
    op.drop_table("audit_event_basic")
    op.drop_table("refresh_token")
