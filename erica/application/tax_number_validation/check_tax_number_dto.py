from typing import Optional

from erica.application.Shared.response_dto import ResponseBaseDto
from erica.application.base_dto import BaseDto
from erica.domain.tax_number_validation.check_tax_number import CheckTaxNumberPayload


# Input

class CheckTaxNumberDto(BaseDto):
    payload: CheckTaxNumberPayload
    clientIdentifier: str


# Output

class ResultTaxResponseDto(BaseDto):
    is_valid: bool


class TaxResponseDto(ResponseBaseDto):
    result: Optional[ResultTaxResponseDto]
