import sqlalchemy
from sqlalchemy import MetaData, Column, String, text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.domain.Shared.EricaAuftrag import AuftragType
from src.domain.Shared.Status import Status
from src.infrastructure.sqlalchemy.BaseSchema import AuditedSchemaMixin

metadata = MetaData()
BaseDbSchema = declarative_base()


class EricaAuftragSchema(AuditedSchemaMixin, BaseDbSchema):
    __tablename__ = 'erica_auftrag'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"), )
    type = Column(Enum(AuftragType))
    payload = Column(sqlalchemy.types.JSON)
    job_id = Column(UUID(as_uuid=True))
    elster_request_id = Column(String, nullable=True)
    status = Column(Enum(Status))
