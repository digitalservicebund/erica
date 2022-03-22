import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.sql.functions import current_timestamp


class AuditedSchemaMixin(object):
    created_at = Column(sqlalchemy.types.DateTime(timezone=True),
                        default=current_timestamp(),
                        nullable=False)
    updated_at = Column(sqlalchemy.types.DateTime(timezone=True),
                        default=current_timestamp(),
                        onupdate=current_timestamp(),
                        nullable=False)
    creator_id = Column(String)
