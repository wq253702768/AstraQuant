from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0001_alert_schema"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
 op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
 for t in ["alert_rule","alert_event","alert_notification","alert_acknowledgement","alert_suppression"]:
  op.create_table(t, sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True,server_default=sa.text("uuid_generate_v4()")), sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
def downgrade():
 for t in ["alert_suppression","alert_acknowledgement","alert_notification","alert_event","alert_rule"]: op.drop_table(t)
