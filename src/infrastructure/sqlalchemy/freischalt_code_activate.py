from sqlalchemy import MetaData, Column, String, Enum, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.domain.freischalt_code import Status
from src.infrastructure.sqlalchemy.base_entity import AuditedEntityMixin

metadata = MetaData()
BaseDbEntity = declarative_base()


class FreischaltCodeActivateEntity(AuditedEntityMixin, BaseDbEntity):
    __tablename__ = 'freischalt_code_activate'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"), )
    tax_ident = Column(String)
    elster_request_id = Column(String, nullable=True)
    freischalt_code = Column(String)
    status = Column(Enum(Status))
