from abc import ABCMeta, ABC
from uuid import UUID

from pydantic import BaseModel

from src.domain.base_domain_model import BaseDomainModel, BaseRepositoryInterface
from src.domain.status import Status


class TaxDeclarationPayload(BaseModel):
    name: str
    last_name: str
    tax_ident: str


class TaxDeclaration(BaseDomainModel[UUID]):
    status: Status = Status.new
    payload: TaxDeclarationPayload
    user_id: UUID

    class Config:
        orm_mode = True


class TaxDeclarationRepositoryInterface(BaseRepositoryInterface[TaxDeclaration], ABC):
    __metaclass__ = ABCMeta
