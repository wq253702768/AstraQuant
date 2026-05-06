from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0001_live_monitor_schema"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
 op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
 for table in ["live_equity_curve","live_account_daily_summary","live_strategy_daily_summary","live_risk_daily_summary","live_observation","live_admission_result","live_daily_report"]:
  op.create_table(table, sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True,server_default=sa.text("uuid_generate_v4()")), sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
def downgrade():
 for table in ["live_daily_report","live_admission_result","live_observation","live_risk_daily_summary","live_strategy_daily_summary","live_account_daily_summary","live_equity_curve"]:
  op.drop_table(table)
