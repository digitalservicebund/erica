from abc import ABC
from datetime import date
from typing import Optional

from erica.domain.model.base_domain_model import BasePayload


class FreischaltCodeRequestPayload(BasePayload, ABC):
    tax_id_number: str
    date_of_birth: date
    tax_year: Optional[str]


class FreischaltCodeActivatePayload(BasePayload, ABC):
    tax_id_number: Optional[str]
    freischalt_code: str
    elster_request_id: str


class FreischaltCodeRevocatePayload(BasePayload, ABC):
    tax_id_number: Optional[str]
    elster_request_id: str
