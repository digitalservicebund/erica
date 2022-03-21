from abc import ABCMeta
from uuid import UUID

from pydantic.main import BaseModel

from erica.domain.Shared.BaseDomainModel import BaseDomainModel
from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.domain.Shared.Status import Status


class BasePayload(BaseModel):
    __metaclass__ = ABCMeta


class EricaRequest(BaseDomainModel[UUID]):
    type: AuftragType
    status: Status = Status.new
    payload: object
    job_id: UUID
    elster_request_id: str = None

    class Config:
        orm_mode = True
