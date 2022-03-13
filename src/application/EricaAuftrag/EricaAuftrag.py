from uuid import UUID

from pydantic.main import BaseModel

from src.domain.Shared.EricaAuftrag import AuftragType
from src.domain.Shared.Status import Status


class BasePayloadDto(BaseModel):
    pass


class EricaAuftragDto(BaseModel):
    type: AuftragType
    status: Status = Status.new
    payload: BasePayloadDto
    job_id: UUID
    elster_request_id: str = None
