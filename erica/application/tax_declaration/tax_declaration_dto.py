from typing import Optional, Union

from erica.application.Shared.response_dto import ResponseBaseDto, ResultTransferPdfResponseDto, \
    ResultValidationErrorResponseDto
from erica.application.base_dto import BaseDto
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class TaxDeclarationPayloadDto(BaseDto):
    est_data: FormDataEst
    meta_data: MetaDataEst


# Input

class TaxDeclarationDto(BaseDto):
    payload: TaxDeclarationPayloadDto
    client_identifier: str


# Output

class EstResponseDto(ResponseBaseDto):
    result: Optional[Union[ResultTransferPdfResponseDto, ResultValidationErrorResponseDto]]
