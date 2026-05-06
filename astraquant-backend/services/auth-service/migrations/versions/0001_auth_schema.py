"""create auth schema

Revision ID: 0001_auth_schema
Revises:
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_auth_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("user_account", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("username", sa.String(64), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("display_name", sa.String(128), nullable=False), sa.Column("email", sa.String(128)), sa.Column("phone", sa.String(32)), sa.Column("status", sa.String(32), nullable=False, server_default="active"), sa.Column("last_login_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("uk_user_username", "user_account", ["username"], unique=True)
    op.create_index("idx_user_status", "user_account", ["status"])
    op.create_table("role", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("code", sa.String(64), nullable=False, unique=True), sa.Column("name", sa.String(128), nullable=False), sa.Column("description", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("permission", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("code", sa.String(128), nullable=False, unique=True), sa.Column("name", sa.String(128), nullable=False), sa.Column("resource", sa.String(64), nullable=False), sa.Column("action", sa.String(64), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("user_role", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("user_account.id"), nullable=False), sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("role.id"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("idx_user_role_user", "user_role", ["user_id"])
    op.create_index("idx_user_role_role", "user_role", ["role_id"])
    op.create_table("role_permission", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("role_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("role.id"), nullable=False), sa.Column("permission_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("permission.id"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("idx_role_permission_role", "role_permission", ["role_id"])
    op.create_index("idx_role_permission_permission", "role_permission", ["permission_id"])
    op.create_table("login_log", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("user_id", postgresql.UUID(as_uuid=True)), sa.Column("username", sa.String(64), nullable=False), sa.Column("success", sa.Boolean(), nullable=False), sa.Column("failure_reason", sa.Text()), sa.Column("ip_address", sa.String(64)), sa.Column("user_agent", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("idx_login_log_created_at", "login_log", ["created_at"])

def downgrade() -> None:
    op.drop_table("login_log")
    op.drop_table("role_permission")
    op.drop_table("user_role")
    op.drop_table("permission")
    op.drop_table("role")
    op.drop_table("user_account")
