import sqlalchemy
from sqlalchemy import Column, String


class AuditedEntityMixin(object):
    created_at = Column(sqlalchemy.types.DateTime)
    updated_at = Column(sqlalchemy.types.DateTime)
    creator_id = Column(String)
