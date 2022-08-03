from sqlalchemy import MetaData, Column, String, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base

from erica.domain.Shared.EricaRequest import RequestType
from erica.domain.Shared.Status import Status
from erica.erica_shared.sqlalchemy.base_schema import AuditedSchemaMixin

metadata = MetaData()
BaseDbSchema = declarative_base()


class EricaRequestSchema(AuditedSchemaMixin, BaseDbSchema):
    __tablename__ = 'erica_request'
    id = Column(Integer,
                primary_key=True)
    type = Column(Enum(RequestType))
    payload = Column(JSONB)
    result = Column(JSONB)
    request_id = Column(UUID(as_uuid=True))
    status = Column(Enum(Status))
    error_code = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
