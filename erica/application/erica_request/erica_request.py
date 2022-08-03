from typing import Optional
from uuid import UUID

from erica.application.base_dto import BaseDto
from erica.domain.shared.erica_request import RequestType
from erica.domain.shared.status import Status


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
