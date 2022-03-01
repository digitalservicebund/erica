from uuid import UUID

from pydantic import BaseModel

from src.domain.base_domain_model import BaseDomainModel
from src.domain.status import Status


class FreischaltCodePayload(BaseModel):
    freischalt_code: str
    tax_id: str


class FreischaltCode(BaseDomainModel[UUID]):
    status: Status = Status.new
    payload: FreischaltCodePayload
    user_id: UUID
