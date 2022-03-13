from abc import ABCMeta, ABC
from uuid import UUID

from pydantic.main import BaseModel

from src.domain.Shared.BaseDomainModel import BaseDomainModel
from src.domain.Shared.EricaAuftrag import AuftragType
from src.domain.Shared.Status import Status


class BasePayload(BaseModel):
    __metaclass__ = ABCMeta


class EricaAuftrag(BaseDomainModel[UUID]):
    type: AuftragType
    status: Status = Status.new
    payload: BasePayload
    job_id: UUID
    elster_request_id: str = None

    class Config:
        orm_mode = True
