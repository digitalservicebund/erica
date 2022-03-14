from datetime import date

from pydantic import BaseModel


class BaseDto(BaseModel):
    pass


class FreischaltCodeBeantragenDto(BaseDto):
    tax_ident: str
    date_of_birth: date


class FreischaltCodeRevocateDto(BaseDto):
    tax_ident: str
    elster_request_id: str


class FreischaltCodeActivateDto(BaseDto):
    tax_ident: str
    freischalt_code: str
    elster_request_id: str
