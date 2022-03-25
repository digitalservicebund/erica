from abc import ABC
from datetime import date

from erica.domain.erica_request.erica_request import BasePayload


class FreischaltCodeRequestPayload(BasePayload, ABC):
    tax_ident: str
    dob: date

    class Config:
        orm_mode = True


class FreischaltCodeActivatePayload(BasePayload, ABC):
    tax_ident: str
    freischalt_code: str

    class Config:
        orm_mode = True


class FreischaltCodeRevocatePayload(BasePayload, ABC):
    tax_ident: str

    class Config:
        orm_mode = True
