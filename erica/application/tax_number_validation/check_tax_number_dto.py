from erica.application.base_dto import BaseDto
from erica.domain.tax_number_validation.check_tax_number import CheckTaxNumberPayload, StateAbbreviation


class CheckTaxNumberPayloadDto(BaseDto):
    state_abbreviation: StateAbbreviation
    tax_number: str


class CheckTaxNumberDto(BaseDto):
    payload: CheckTaxNumberPayload
    clientIdentifier: str
