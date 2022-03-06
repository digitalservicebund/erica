from sqlalchemy import MetaData, Column, String, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.domain.FreischaltCode.freischalt_code import Status
from src.infrastructure.sqlalchemy.base_entity import AuditedSchemaMixin

metadata = MetaData()
BaseDbSchema = declarative_base()


class FreischaltCodeRevocateSchema(AuditedSchemaMixin, BaseDbSchema):
    __tablename__ = 'freischalt_code_revocate'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"), )
    tax_ident = Column(String)
    elster_request_id = Column(String, nullable=True)
    status = Column(Enum(Status))
