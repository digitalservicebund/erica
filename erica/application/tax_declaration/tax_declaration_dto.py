from typing import Optional, Union

from erica.application.Shared.response_dto import ResponseBaseDto, ResultTransferPdfResponseDto, \
    ResultValidationErrorResponseDto
from erica.application.base_dto import BaseDto
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


class FormDataEstDto(FormDataEst, BaseDto):
    pass


class MetaDataEstDto(MetaDataEst, BaseDto):
    pass


class TaxDeclarationPayloadDto(BaseDto):
    est_data: FormDataEstDto
    meta_data: MetaDataEstDto


# Input

class TaxDeclarationDto(BaseDto):
    payload: TaxDeclarationPayloadDto
    client_identifier: str


# Output

class EstResponseDto(ResponseBaseDto):
    result: Optional[Union[ResultTransferPdfResponseDto, ResultValidationErrorResponseDto]]
