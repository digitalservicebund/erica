from uuid import UUID

from pydantic.main import BaseModel

from erica.domain.Shared.EricaAuftrag import AuftragType
from erica.domain.Shared.Status import Status


class BasePayloadDto(BaseModel):
    pass


class EricaAuftragDto(BaseModel):
    type: AuftragType
    status: Status = Status.new
    payload: object
    job_id: UUID
    elster_request_id: str = None
