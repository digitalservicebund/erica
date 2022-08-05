from enum import Enum
from typing import Optional
from uuid import UUID

from erica.domain.model.base_domain_model import BaseDomainModel


class RequestType(int, Enum):
    freischalt_code_request = 0
    freischalt_code_activate = 1
    freischalt_code_revocate = 2
    check_tax_number = 3
    send_est = 4
    grundsteuer = 5


class Status(int, Enum):
    new = 0
    scheduled = 1
    processing = 2
    failed = 3
    success = 4


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
