from erica.application.base_dto import BaseDto
from erica.domain.TaxDeclaration.TaxDeclaration import TaxDeclarationPayload


class TaxDeclarationDto(BaseDto):
    payload: TaxDeclarationPayload
    clientIdentifier: str
