from typing import Optional

from erica.application.Shared.response_dto import ResponseBaseDto
from erica.application.base_dto import BaseDto
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class TaxDeclarationPayloadDto(BaseDto):
    est_data: FormDataEst
    meta_data: MetaDataEst


# Input

class TaxDeclarationDto(BaseDto):
    payload: TaxDeclarationPayloadDto
    clientIdentifier: str


# Output

class ResultEstResponseDto(BaseDto):
    transfer_ticket: str
    pdf: str


class EstResponseDto(ResponseBaseDto):
    result: Optional[ResultEstResponseDto]
