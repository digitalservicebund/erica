from sqlalchemy import MetaData, Column, String, text, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.domain.FreischaltCode.freischalt_code import Status
from src.infrastructure.sqlalchemy.base_entity import AuditedEntityMixin

metadata = MetaData()
BaseDbEntity = declarative_base()


class FreischaltCodeEntity(AuditedEntityMixin, BaseDbEntity):
    __tablename__ = 'freischalt_code'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"), )
    tax_ident = Column(String)
    job_id = Column(UUID(as_uuid=True))
    elster_request_id = Column(String, nullable=True)
    date_of_birth = Column(DateTime)
    status = Column(Enum(Status))
