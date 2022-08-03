from datetime import date

from typing import Optional

from erica.erica_api.dto.response_dto import ResponseBaseDto
from erica.erica_api.dto.base_dto import BaseDto


# Input
from erica.erica_api.dto.tax_id_number import TaxIdNumber


class FreischaltCodeRequestPayloadDto(BaseDto):
    tax_id_number: TaxIdNumber
    date_of_birth: date
    tax_year: Optional[str]


class FreischaltCodeActivatePayloadDto(BaseDto):
    tax_id_number: Optional[TaxIdNumber]
    freischalt_code: str
    elster_request_id: str


class FreischaltCodeRequestDto(BaseDto):
    payload: FreischaltCodeRequestPayloadDto
    client_identifier: str


class FreischaltCodeActivateDto(BaseDto):
    payload: FreischaltCodeActivatePayloadDto
    client_identifier: str


class FreischaltCodeRevocatePayloadDto(BaseDto):
    tax_id_number: Optional[TaxIdNumber]
    elster_request_id: str


class FreischaltCodeRevocateDto(BaseDto):
    payload: FreischaltCodeRevocatePayloadDto
    client_identifier: str


# Output

class TransferticketAndIdnrResponseDto(BaseDto):
    transferticket: str
    tax_id_number: Optional[str]


class ResultFreischaltcodeRequestAndActivationDto(TransferticketAndIdnrResponseDto):
    elster_request_id: str


class FreischaltcodeRequestAndActivationResponseDto(ResponseBaseDto):
    result: Optional[ResultFreischaltcodeRequestAndActivationDto]


class FreischaltcodeRevocationResponseDto(ResponseBaseDto):
    result: Optional[TransferticketAndIdnrResponseDto]
