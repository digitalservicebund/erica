from erica.application.base_dto import BaseDto
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class TaxDeclarationPayloadDto(BaseDto):
    est_data: FormDataEst
    meta_data: MetaDataEst


class TaxDeclarationDto(BaseDto):
    payload: TaxDeclarationPayloadDto
    clientIdentifier: str
