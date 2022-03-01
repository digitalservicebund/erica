from uuid import UUID

from pydantic import BaseModel

from src.domain.status import Status


class TaxIdentCreateDto(BaseModel):
    tax_ident: str
    user_id: UUID

    class Config:
        orm_mode = True


class TaxIdentDto(BaseModel):
    id: UUID
    status: Status
    tax_ident: str
    user_id: UUID

    class Config:
        orm_mode = True


class TaxIdentValidateDto(BaseModel):
    tax_ident: str
    user_id: UUID

    class Config:
        orm_mode = True
