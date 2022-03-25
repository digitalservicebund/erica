from erica.application.base_dto import BaseDto
from erica.domain.tax_number_validation.check_tax_number import CheckTaxNumberPayload


class CheckTaxNumberDto(BaseDto):
    payload: CheckTaxNumberPayload
    clientIdentifier: str
