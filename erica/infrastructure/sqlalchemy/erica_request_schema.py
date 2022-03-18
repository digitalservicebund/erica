from sqlalchemy import MetaData, Column, String, text, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base

from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.domain.Shared.Status import Status
from erica.infrastructure.sqlalchemy.base_schema import AuditedSchemaMixin

metadata = MetaData()
BaseDbSchema = declarative_base()


class EricaRequestSchema(AuditedSchemaMixin, BaseDbSchema):
    __tablename__ = 'erica_auftrag'
    id = Column(Integer,
                primary_key=True)
    type = Column(Enum(AuftragType))
    payload = Column(JSONB)
    job_id = Column(UUID(as_uuid=True))
    elster_request_id = Column(String, nullable=True)
    status = Column(Enum(Status))
