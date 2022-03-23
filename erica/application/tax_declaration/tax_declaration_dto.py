from erica.application.base_dto import BaseDto
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class TaxDeclarationDto(BaseDto):
    est_data: FormDataEst
    meta_data: MetaDataEst
