import uuid
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB

from erica.domain.Shared.Status import Status
from erica.erica_shared.sqlalchemy.erica_request_schema import BaseDbSchema


class MockDomainModel(BaseModel):
    request_id: Optional[uuid.UUID]
    payload: dict
    status: Status = Status.new

    class Config:
        orm_mode = True


class MockSchema(BaseDbSchema):
    __tablename__ = 'mock_schema'
    id = Column(Integer,
                primary_key=True)
    request_id = Column(UUID(as_uuid=True))
    payload = Column(JSONB)
    status = Column(Enum(Status))
