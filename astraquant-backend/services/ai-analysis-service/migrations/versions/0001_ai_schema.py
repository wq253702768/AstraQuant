"""create ai analysis schema

Revision ID: 0001_ai_schema
Revises:
Create Date: 2026-05-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_ai_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("ai_task", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("task_type", sa.String(64), nullable=False), sa.Column("related_task_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("strategy_id", postgresql.UUID(as_uuid=True)), sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True)), sa.Column("status", sa.String(64), nullable=False), sa.Column("current_agent", sa.String(128)), sa.Column("progress", sa.Numeric(5,2), nullable=False, server_default="0"), sa.Column("input_data_hash", sa.String(128)), sa.Column("result_json", postgresql.JSONB), sa.Column("error_message", sa.Text()), sa.Column("created_by", postgresql.UUID(as_uuid=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_ai_task_related_task", "ai_task", ["related_task_id"])
    op.create_index("idx_ai_task_status", "ai_task", ["status"])
    op.create_index("idx_ai_task_strategy_version", "ai_task", ["strategy_version_id"])
    op.create_index("idx_ai_task_created_at", "ai_task", ["created_at"])
    op.create_table("ai_agent_output", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("ai_task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ai_task.id"), nullable=False), sa.Column("agent_name", sa.String(128), nullable=False), sa.Column("conclusion", sa.Text()), sa.Column("evidence_json", postgresql.JSONB), sa.Column("suggestions_json", postgresql.JSONB), sa.Column("risk_level", sa.String(32)), sa.Column("confidence", sa.Numeric(8,4)), sa.Column("output_json", postgresql.JSONB, nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_ai_agent_output_task", "ai_agent_output", ["ai_task_id"])
    op.create_index("idx_ai_agent_output_agent", "ai_agent_output", ["agent_name"])
    op.create_table("ai_model_call_log", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("ai_task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("ai_task.id"), nullable=False), sa.Column("agent_name", sa.String(128), nullable=False), sa.Column("model_provider", sa.String(64), nullable=False), sa.Column("model_name", sa.String(128), nullable=False), sa.Column("model_version", sa.String(128)), sa.Column("temperature", sa.Numeric(8,4)), sa.Column("max_context", sa.Integer()), sa.Column("input_tokens", sa.Integer()), sa.Column("output_tokens", sa.Integer()), sa.Column("prompt_version", sa.String(64)), sa.Column("input_data_hash", sa.String(128)), sa.Column("latency_ms", sa.Integer()), sa.Column("request_json", postgresql.JSONB), sa.Column("output_json", postgresql.JSONB), sa.Column("error_message", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_ai_model_call_task", "ai_model_call_log", ["ai_task_id"])
    op.create_index("idx_ai_model_call_agent", "ai_model_call_log", ["agent_name"])
    op.create_index("idx_ai_model_call_created_at", "ai_model_call_log", ["created_at"])
    op.create_table("ai_prompt_version", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("prompt_code", sa.String(128), nullable=False), sa.Column("version", sa.String(32), nullable=False), sa.Column("agent_name", sa.String(128), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("output_schema", postgresql.JSONB), sa.Column("description", sa.Text()), sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("uk_ai_prompt_version", "ai_prompt_version", ["prompt_code", "version"], unique=True)
    op.create_index("idx_ai_prompt_enabled", "ai_prompt_version", ["enabled"])
    op.create_index("idx_ai_prompt_agent", "ai_prompt_version", ["agent_name"])

def downgrade() -> None:
    op.drop_table("ai_prompt_version")
    op.drop_table("ai_model_call_log")
    op.drop_table("ai_agent_output")
    op.drop_table("ai_task")
