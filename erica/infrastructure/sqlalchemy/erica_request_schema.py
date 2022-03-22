from sqlalchemy import MetaData, Column, String, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base

from erica.domain.Shared.EricaAuftrag import RequestType
from erica.domain.Shared.Status import Status
from erica.infrastructure.sqlalchemy.base_schema import AuditedSchemaMixin

metadata = MetaData()
BaseDbSchema = declarative_base()


class EricaRequestSchema(AuditedSchemaMixin, BaseDbSchema):
    __tablename__ = 'erica_request'
    id = Column(Integer,
                primary_key=True)
    type = Column(Enum(RequestType))
    payload = Column(JSONB)
    result = Column(JSONB)
    job_id = Column(UUID(as_uuid=True))
    status = Column(Enum(Status))
