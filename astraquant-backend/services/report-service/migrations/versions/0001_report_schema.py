from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision = "0001_report_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    op.create_table("report_task", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("report_type", sa.String(64), nullable=False), sa.Column("related_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("formats", postgresql.JSONB, nullable=False), sa.Column("status", sa.String(64), nullable=False), sa.Column("progress", sa.Numeric(5,2), nullable=False, server_default="0"), sa.Column("current_stage", sa.String(64)), sa.Column("error_message", sa.Text()), sa.Column("created_by", postgresql.UUID(as_uuid=True)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_report_task_related", "report_task", ["related_id"])
    op.create_index("idx_report_task_status", "report_task", ["status"])
    op.create_index("idx_report_task_created_at", "report_task", ["created_at"])
    op.create_table("report_file", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("uuid_generate_v4()")), sa.Column("report_task_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("report_task.id"), nullable=False), sa.Column("report_type", sa.String(64), nullable=False), sa.Column("related_id", postgresql.UUID(as_uuid=True), nullable=False), sa.Column("file_format", sa.String(16), nullable=False), sa.Column("bucket_name", sa.String(128), nullable=False), sa.Column("object_key", sa.String(512), nullable=False), sa.Column("file_url", sa.Text()), sa.Column("file_size", sa.BigInteger()), sa.Column("content_hash", sa.String(128)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.create_index("idx_report_file_task", "report_file", ["report_task_id"])
    op.create_index("idx_report_file_related", "report_file", ["related_id"])
    op.create_index("idx_report_file_type", "report_file", ["report_type"])
def downgrade():
    op.drop_table("report_file")
    op.drop_table("report_task")
