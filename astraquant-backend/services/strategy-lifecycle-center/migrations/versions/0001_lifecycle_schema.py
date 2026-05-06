from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_lifecycle_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table(
        "strategy_lifecycle_state",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("current_stage", sa.String(64), nullable=False),
        sa.Column("current_status", sa.String(64), nullable=False),
        sa.Column("backtest_id", postgresql.UUID(as_uuid=True)),
        sa.Column("ai_analysis_id", postgresql.UUID(as_uuid=True)),
        sa.Column("strategy_score_id", postgresql.UUID(as_uuid=True)),
        sa.Column("simulation_observation_id", postgresql.UUID(as_uuid=True)),
        sa.Column("simulation_admission_result_id", postgresql.UUID(as_uuid=True)),
        sa.Column("live_observation_id", postgresql.UUID(as_uuid=True)),
        sa.Column("live_admission_result_id", postgresql.UUID(as_uuid=True)),
        sa.Column("latest_approval_id", postgresql.UUID(as_uuid=True)),
        sa.Column("latest_gate_result", sa.String(64)),
        sa.Column("latest_gate_reason", sa.Text()),
        sa.Column("live_enabled", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("scale_up_allowed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("retired", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("risk_level", sa.String(32)),
        sa.Column("lifecycle_score", sa.Numeric(8, 2)),
        sa.Column("created_by", postgresql.UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("uk_strategy_lifecycle_state", "strategy_lifecycle_state", ["strategy_version_id"], unique=True)
    op.create_index("idx_lifecycle_status", "strategy_lifecycle_state", ["current_status"])
    op.create_index("idx_lifecycle_stage", "strategy_lifecycle_state", ["current_stage"])
    op.create_index("idx_lifecycle_strategy", "strategy_lifecycle_state", ["strategy_id", "strategy_version_id"])

    op.create_table(
        "lifecycle_event",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(128), nullable=False),
        sa.Column("from_status", sa.String(64)),
        sa.Column("to_status", sa.String(64)),
        sa.Column("trigger_source", sa.String(64), nullable=False),
        sa.Column("trigger_resource_type", sa.String(64)),
        sa.Column("trigger_resource_id", sa.String(128)),
        sa.Column("reason", sa.Text()),
        sa.Column("evidence_json", postgresql.JSONB()),
        sa.Column("metadata_json", postgresql.JSONB()),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True)),
        sa.Column("trace_id", sa.String(128)),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_lifecycle_event_strategy", "lifecycle_event", ["strategy_version_id"])
    op.create_index("idx_lifecycle_event_type", "lifecycle_event", ["event_type"])
    op.create_index("idx_lifecycle_event_time", "lifecycle_event", ["occurred_at"])
    op.create_index("idx_lifecycle_event_trace", "lifecycle_event", ["trace_id"])

    op.create_table(
        "lifecycle_approval",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("approval_type", sa.String(64), nullable=False),
        sa.Column("approval_status", sa.String(64), nullable=False),
        sa.Column("requested_by", postgresql.UUID(as_uuid=True)),
        sa.Column("requested_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("approved_by", postgresql.UUID(as_uuid=True)),
        sa.Column("approved_at", sa.DateTime(timezone=True)),
        sa.Column("rejected_by", postgresql.UUID(as_uuid=True)),
        sa.Column("rejected_at", sa.DateTime(timezone=True)),
        sa.Column("request_reason", sa.Text()),
        sa.Column("approval_comment", sa.Text()),
        sa.Column("rejection_reason", sa.Text()),
        sa.Column("evidence_json", postgresql.JSONB()),
        sa.Column("risk_summary_json", postgresql.JSONB()),
        sa.Column("expires_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_lifecycle_approval_strategy", "lifecycle_approval", ["strategy_version_id"])
    op.create_index("idx_lifecycle_approval_type", "lifecycle_approval", ["approval_type"])
    op.create_index("idx_lifecycle_approval_status", "lifecycle_approval", ["approval_status"])

    op.create_table(
        "lifecycle_evidence",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("evidence_type", sa.String(64), nullable=False),
        sa.Column("resource_type", sa.String(64), nullable=False),
        sa.Column("resource_id", sa.String(128), nullable=False),
        sa.Column("title", sa.String(256)),
        sa.Column("summary", sa.Text()),
        sa.Column("score", sa.Numeric(8, 2)),
        sa.Column("passed", sa.Boolean()),
        sa.Column("evidence_json", postgresql.JSONB()),
        sa.Column("object_key", sa.String(512)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_lifecycle_evidence_strategy", "lifecycle_evidence", ["strategy_version_id"])
    op.create_index("idx_lifecycle_evidence_type", "lifecycle_evidence", ["evidence_type"])
    op.create_index("idx_lifecycle_evidence_resource", "lifecycle_evidence", ["resource_type", "resource_id"])

    op.create_table(
        "lifecycle_task",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("task_type", sa.String(64), nullable=False),
        sa.Column("task_status", sa.String(64), nullable=False),
        sa.Column("title", sa.String(256), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True)),
        sa.Column("due_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("completed_by", postgresql.UUID(as_uuid=True)),
        sa.Column("related_resource_type", sa.String(64)),
        sa.Column("related_resource_id", sa.String(128)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_lifecycle_task_strategy", "lifecycle_task", ["strategy_version_id"])
    op.create_index("idx_lifecycle_task_status", "lifecycle_task", ["task_status"])
    op.create_index("idx_lifecycle_task_owner", "lifecycle_task", ["owner_id"])

    op.create_table(
        "lifecycle_stage_gate_result",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column("strategy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("strategy_version_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("gate_code", sa.String(128), nullable=False),
        sa.Column("gate_name", sa.String(128), nullable=False),
        sa.Column("result", sa.String(64), nullable=False),
        sa.Column("from_status", sa.String(64)),
        sa.Column("target_status", sa.String(64)),
        sa.Column("passed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("reject_reasons", postgresql.JSONB()),
        sa.Column("warnings", postgresql.JSONB()),
        sa.Column("suggestions", postgresql.JSONB()),
        sa.Column("evidence_json", postgresql.JSONB()),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("trace_id", sa.String(128)),
    )
    op.create_index("idx_stage_gate_strategy", "lifecycle_stage_gate_result", ["strategy_version_id"])
    op.create_index("idx_stage_gate_code", "lifecycle_stage_gate_result", ["gate_code"])
    op.create_index("idx_stage_gate_result", "lifecycle_stage_gate_result", ["result"])


def downgrade():
    for table in [
        "lifecycle_stage_gate_result",
        "lifecycle_task",
        "lifecycle_evidence",
        "lifecycle_approval",
        "lifecycle_event",
        "strategy_lifecycle_state",
    ]:
        op.drop_table(table)
