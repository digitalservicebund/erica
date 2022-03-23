from abc import ABCMeta
from typing import Optional
from uuid import UUID

from pydantic.main import BaseModel

from erica.domain.Shared.BaseDomainModel import BaseDomainModel
from erica.domain.Shared.EricaAuftrag import RequestType
from erica.domain.Shared.Status import Status


class BasePayload(BaseModel):
    __metaclass__ = ABCMeta


class EricaRequest(BaseDomainModel[UUID]):
    type: RequestType
    status: Status = Status.new
    payload: object
    request_id: UUID
    result: Optional[object]
    error_code: Optional[str]
    error_message: Optional[str]

    class Config:
        orm_mode = True

    def __str__(self):
        return f"EricaAuftrag(type={self.type}, request_id={self.request_id}, status={self.status}"
