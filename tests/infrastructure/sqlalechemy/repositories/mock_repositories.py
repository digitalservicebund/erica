import uuid
from typing import Optional

import sqlalchemy
from pydantic import BaseModel
import datetime
from sqlalchemy import Column, Integer, Enum, String
from sqlalchemy.dialects.postgresql import UUID, JSONB

from erica.domain.Shared.Status import Status
from erica.infrastructure.sqlalchemy.erica_request_schema import BaseDbSchema


class MockDomainModel(BaseModel):
    request_id: Optional[uuid.UUID]
    payload: dict
    status: Status = Status.new
    updated_at: Optional[datetime.datetime]
    error_code: Optional[str]
    error_message: Optional[str]

    class Config:
        orm_mode = True


class MockSchema(BaseDbSchema):
    __tablename__ = 'mock_schema'
    id = Column(Integer,
                primary_key=True)
    request_id = Column(UUID(as_uuid=True))
    payload = Column(JSONB)
    status = Column(Enum(Status))
    updated_at = Column(sqlalchemy.types.DateTime(timezone=True))
    error_code = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
