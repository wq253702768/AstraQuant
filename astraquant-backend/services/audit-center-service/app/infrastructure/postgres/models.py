from datetime import datetime
from uuid import uuid4
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.postgres.base import Base
class AuditEventModel(Base):
    __tablename__="audit_event"; id:Mapped[str]=mapped_column(UUID(as_uuid=False),primary_key=True,default=lambda:str(uuid4())); event_type:Mapped[str]=mapped_column(String(128),index=True); level:Mapped[str]=mapped_column(String(32)); actor_type:Mapped[str|None]=mapped_column(String(64)); actor_id:Mapped[str|None]=mapped_column(UUID(as_uuid=False)); resource_type:Mapped[str]=mapped_column(String(64)); resource_id:Mapped[str]=mapped_column(String(128)); action:Mapped[str]=mapped_column(String(128)); before_json:Mapped[dict|None]=mapped_column(JSONB); after_json:Mapped[dict|None]=mapped_column(JSONB); metadata_json:Mapped[dict|None]=mapped_column(JSONB); trace_id:Mapped[str|None]=mapped_column(String(128),index=True); occurred_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class AuditTraceModel(Base):
    __tablename__="audit_trace"; id:Mapped[str]=mapped_column(UUID(as_uuid=False),primary_key=True,default=lambda:str(uuid4())); trace_id:Mapped[str]=mapped_column(String(128),unique=True); event_count:Mapped[int]=mapped_column(default=0); summary_json:Mapped[dict|None]=mapped_column(JSONB); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class AuditExportTaskModel(Base):
    __tablename__="audit_export_task"; id:Mapped[str]=mapped_column(UUID(as_uuid=False),primary_key=True,default=lambda:str(uuid4())); export_type:Mapped[str]=mapped_column(String(64)); status:Mapped[str]=mapped_column(String(64)); filter_json:Mapped[dict]=mapped_column(JSONB); file_format:Mapped[str]=mapped_column(String(16)); object_key:Mapped[str|None]=mapped_column(String(512)); file_url:Mapped[str|None]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
class AuditEvidenceModel(Base):
    __tablename__="audit_evidence"; id:Mapped[str]=mapped_column(UUID(as_uuid=False),primary_key=True,default=lambda:str(uuid4())); trace_id:Mapped[str|None]=mapped_column(String(128)); audit_event_id:Mapped[str]=mapped_column(UUID(as_uuid=False)); evidence_type:Mapped[str]=mapped_column(String(64)); evidence_json:Mapped[dict|None]=mapped_column(JSONB); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now())
