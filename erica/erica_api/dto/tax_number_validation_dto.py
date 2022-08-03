from typing import Optional

from erica.erica_api.dto.response_dto import ResponseBaseDto
from erica.erica_api.dto.base_dto import BaseDto
from erica.erica_shared.payload.tax_number_validation import StateAbbreviation


class CheckTaxNumberPayloadDto(BaseDto):
    state_abbreviation: StateAbbreviation
    tax_number: str


# Input

class CheckTaxNumberDto(BaseDto):
    payload: CheckTaxNumberPayloadDto
    client_identifier: str


# Output

class ResultTaxResponseDto(BaseDto):
    is_valid: bool


class TaxResponseDto(ResponseBaseDto):
    result: Optional[ResultTaxResponseDto]
