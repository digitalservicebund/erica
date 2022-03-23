import datetime
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

DataT = TypeVar('DataT')
ClassT = TypeVar('ClassT')


class AuditedModel(BaseModel):
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    creator_id: str


class BaseDomainModel(AuditedModel, Generic[DataT]):
    id: Optional[DataT] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BasePayload(BaseModel):
    pass
