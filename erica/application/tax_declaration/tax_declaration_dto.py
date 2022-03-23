from pydantic.main import BaseModel

from erica.application.base_dto import BaseDto
from erica.domain.TaxDeclaration.TaxDeclaration import TaxDeclarationPayload
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class TaxDeclarationDto(BaseModel):
    ttlInMinutes: int
    payload: TaxDeclarationPayload