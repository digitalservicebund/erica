from abc import ABC
from datetime import date

from erica.domain.EricaAuftrag.EricaAuftrag import BasePayload


class FreischaltCodeBeantragenPayload(BasePayload, ABC):
    tax_ident: str
    date_of_birth: date

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
