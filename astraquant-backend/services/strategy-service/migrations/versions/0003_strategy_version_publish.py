"""strategy version publish fields

Revision ID: 0003_strategy_version_publish
Revises: 0002_strategy_core_acceptance
Create Date: 2026-05-07
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0003_strategy_version_publish"
down_revision = "0002_strategy_core_acceptance"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("strategy_version", sa.Column("config_hash", sa.String(128), nullable=True))
    op.add_column("strategy_version", sa.Column("published_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("strategy_version", sa.Column("published_by", postgresql.UUID(as_uuid=True), nullable=True))


def downgrade() -> None:
    op.drop_column("strategy_version", "published_by")
    op.drop_column("strategy_version", "published_at")
    op.drop_column("strategy_version", "config_hash")
