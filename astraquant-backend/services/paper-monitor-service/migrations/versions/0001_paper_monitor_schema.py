from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0001_paper_monitor_schema"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
 op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
 for table in ["paper_equity_curve","paper_strategy_daily_summary","paper_risk_event_summary","simulation_observation","simulation_admission_result","simulation_daily_report"]:
  op.create_table(table, sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True,server_default=sa.text("uuid_generate_v4()")), sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
def downgrade():
 for table in ["simulation_daily_report","simulation_admission_result","simulation_observation","paper_risk_event_summary","paper_strategy_daily_summary","paper_equity_curve"]:
  op.drop_table(table)
