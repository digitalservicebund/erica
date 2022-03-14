import datetime
from typing import TypeVar, Generic, Optional

from pydantic import BaseModel

DataT = TypeVar('DataT')
ClassT = TypeVar('ClassT')


class AuditedModel(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime
    creator_id: str


class BaseDomainModel(AuditedModel, Generic[DataT]):
    id: Optional[DataT]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
