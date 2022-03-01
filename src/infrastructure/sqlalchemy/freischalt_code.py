import sqlalchemy
from sqlalchemy import MetaData, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from src.domain.freischalt_code import Status

metadata = MetaData()
BaseDbEntity = declarative_base()


class FreischaltCodeEntity(BaseDbEntity):
    __tablename__ = 'freischalt_code'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"), )
    user_id = Column(String)
    payload = Column(sqlalchemy.types.JSON)
    status = Column(sqlalchemy.Enum(Status))
