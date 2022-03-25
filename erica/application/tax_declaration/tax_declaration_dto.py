from pydantic import BaseModel
from erica.domain.TaxDeclaration.TaxDeclaration import TaxDeclarationPayload


class TaxDeclarationDto(BaseModel):
    payload: TaxDeclarationPayload
    clientIdentifier: str
