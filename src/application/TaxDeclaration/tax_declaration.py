from uuid import UUID

from pydantic import BaseModel

from src.domain.TaxDeclaration.tax_declaration import TaxDeclarationPayload
from src.domain.Shared.status import Status


class TaxDeclarationCreateDto(BaseModel):
    payload: TaxDeclarationPayload
    user_id: UUID

    class Config:
        orm_mode = True


class TaxDeclarationDto(BaseModel):
    id: UUID
    status: Status
    payload: TaxDeclarationPayload
    user_id: UUID

    class Config:
        orm_mode = True


class TaxDeclarationValidateDto(BaseModel):
    payload: TaxDeclarationPayload
    user_id: UUID

    class Config:
        orm_mode = True