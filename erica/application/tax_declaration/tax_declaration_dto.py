from typing import Optional

from erica.application.Shared.response_dto import ResponseBaseDto
from erica.application.base_dto import BaseDto
from erica.domain.TaxDeclaration.TaxDeclaration import TaxDeclarationPayload


# Input

class TaxDeclarationDto(BaseDto):
    payload: TaxDeclarationPayload
    clientIdentifier: str


# Output

class ResultEstResponseDto(BaseDto):
    transfer_ticket: str
    pdf: str


class EstResponseDto(ResponseBaseDto):
    result: Optional[ResultEstResponseDto]
