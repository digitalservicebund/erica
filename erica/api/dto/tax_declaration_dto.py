from typing import Optional, Union

from erica.api.dto.response_dto import ResponseBaseDto, ResultTransferPdfResponseDto, \
    ResultValidationErrorResponseDto
from erica.api.dto.base_dto import BaseDto
from erica.worker.request_processing.erica_input.v1.erica_input import FormDataEst, MetaDataEst


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
