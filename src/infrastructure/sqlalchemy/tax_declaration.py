import datetime

import sqlalchemy
from sqlalchemy import MetaData, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.domain.tax_declaration import Status
from src.infrastructure.sqlalchemy.base_entity import AuditedEntityMixin

metadata = MetaData()
BaseDbEntity = declarative_base()


class TaxDeclarationEntity(AuditedEntityMixin, BaseDbEntity):
    __tablename__ = 'tax_declarations'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"), )
    user_id = Column(String)
    payload = Column(sqlalchemy.types.JSON)
    status = Column(sqlalchemy.Enum(Status))
