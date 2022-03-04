from datetime import date
from uuid import UUID

from pydantic import BaseModel

from src.domain.status import Status


class FreischaltCodeCreateDto(BaseModel):
    tax_ident: str
    date_of_birth: date

    class Config:
        orm_mode = True


class FreischaltCodeDto(BaseModel):
    id: UUID
    status: Status
    tax_ident: str
    date_of_birth: date

    class Config:
        orm_mode = True


class FreischaltCodeRevocateDto(BaseModel):
    id: UUID
    status: Status
    tax_ident: str
    elster_request_id: str

    class Config:
        orm_mode = True


class FreischaltCodeCreateRevocateDto(BaseModel):
    tax_ident: str
    elster_request_id: str

    class Config:
        orm_mode = True


class FreischaltCodeActivateDto(BaseModel):
    id: UUID
    status: Status
    tax_ident: str
    freischalt_code: str
    elster_request_id: str

    class Config:
        orm_mode = True


class FreischaltCodeCreateActivateDto(BaseModel):
    tax_ident: str
    freischalt_code: str
    elster_request_id: str

    class Config:
        orm_mode = True
