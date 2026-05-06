from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
revision="0001_exchange_account_schema"
down_revision=None
branch_labels=None
depends_on=None
def upgrade():
 op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
 for table in ["exchange_account","exchange_api_credential","account_state_snapshot","position_state_snapshot","order_state_snapshot","credential_audit_log"]:
  op.create_table(table, sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True,server_default=sa.text("uuid_generate_v4()")), sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.func.now(),nullable=False))
def downgrade():
 for table in ["credential_audit_log","order_state_snapshot","position_state_snapshot","account_state_snapshot","exchange_api_credential","exchange_account"]:
  op.drop_table(table)
