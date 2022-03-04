from datetime import date
from uuid import UUID

from src.domain.base_domain_model import BaseDomainModel
from src.domain.status import Status


class FreischaltCode(BaseDomainModel[UUID]):
    status: Status = Status.new
    tax_ident: str
    date_of_birth: date
    elster_request_id: str = None


class FreischaltCodeActivate(BaseDomainModel[UUID]):
    status: Status = Status.new
    tax_ident: str
    freischalt_code: str
    elster_request_id: str = None


class FreischaltCodeRevocate(BaseDomainModel[UUID]):
    status: Status = Status.new
    tax_ident: str
    elster_request_id: str = None
