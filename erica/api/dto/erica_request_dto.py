from typing import Optional
from uuid import UUID

from erica.api.dto.base_dto import BaseDto
from erica.domain.model.erica_request import RequestType, Status


class BasePayloadDto(BaseDto):
    pass


class EricaRequestDto(BaseDto):
    type: RequestType
    status: Status = Status.new
    payload: object
    request_id: UUID
    result: Optional[object]
    error_code: Optional[str]
    error_message: Optional[str]
