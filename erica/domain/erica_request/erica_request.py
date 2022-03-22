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
    job_id: UUID
    result: Optional[object]

    class Config:
        orm_mode = True

    def __str__(self):
        return f"EricaAuftrag(type={self.type}, job_id={self.job_id}, status={self.status}"
