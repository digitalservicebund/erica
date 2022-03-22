import uuid
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from erica.infrastructure.sqlalchemy.erica_request_schema import BaseDbSchema


class MockDomainModel(BaseModel):
    job_id: Optional[uuid.UUID]
    payload: dict

    class Config:
        orm_mode = True


class MockSchema(BaseDbSchema):
    __tablename__ = 'mock_schema'
    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=text("gen_random_uuid()"), )
    job_id = Column(UUID(as_uuid=True))
    payload = Column(JSONB)