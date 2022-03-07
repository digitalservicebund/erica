import sqlalchemy
from sqlalchemy import MetaData, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.domain.TaxDeclaration.TaxDeclaration import Status
from src.infrastructure.sqlalchemy.BaseSchema import AuditedSchemaMixin

metadata = MetaData()
BaseDbSchema = declarative_base()


class TaxDeclarationEntity(AuditedSchemaMixin, BaseDbSchema):
    __tablename__ = 'tax_declarations'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"), )
    user_id = Column(String)
    payload = Column(sqlalchemy.types.JSON)
    status = Column(sqlalchemy.Enum(Status))
