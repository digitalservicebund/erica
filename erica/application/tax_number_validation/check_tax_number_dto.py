from pydantic import BaseModel
from erica.domain.tax_number_validation.check_tax_number import CheckTaxNumberPayload


class CheckTaxNumberDto(BaseModel):
    payload: CheckTaxNumberPayload
    clientIdentifier: str
