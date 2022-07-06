from typing import Optional
from uuid import UUID

from erica.domain.Shared.BaseDomainModel import BaseDomainModel
from erica.domain.Shared.EricaRequest import RequestType
from erica.domain.Shared.Status import Status


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
        return f"EricaRequest(type={self.type.name}, request_id={self.request_id}, status={self.status.name})"
