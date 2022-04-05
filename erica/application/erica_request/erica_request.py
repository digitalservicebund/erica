from typing import Optional
from uuid import UUID

from pydantic.main import BaseModel

from erica.domain.Shared.EricaRequest import RequestType
from erica.domain.Shared.Status import Status


class BasePayloadDto(BaseModel):
    pass


class EricaRequestDto(BaseModel):
    type: RequestType
    status: Status = Status.new
    payload: object
    request_id: UUID
    result: Optional[object]
    error_code: Optional[str]
    error_message: Optional[str]
