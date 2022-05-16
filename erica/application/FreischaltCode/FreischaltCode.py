from datetime import date

from typing import Optional

from erica.application.Shared.response_dto import ResponseBaseDto
from erica.application.base_dto import BaseDto


# Input

class FreischaltCodeRequestPayloadDto(BaseDto):
    tax_id_number: str
    date_of_birth: date


class FreischaltCodeActivatePayloadDto(BaseDto):
    tax_id_number: str
    freischalt_code: str
    elster_request_id: str


class FreischaltCodeRequestDto(BaseDto):
    payload: FreischaltCodeRequestPayloadDto
    client_identifier: str


class FreischaltCodeActivateDto(BaseDto):
    payload: FreischaltCodeActivatePayloadDto
    client_identifier: str


class FreischaltCodeRevocatePayloadDto(BaseDto):
    tax_id_number: str
    elster_request_id: str


class FreischaltCodeRevocateDto(BaseDto):
    payload: FreischaltCodeRevocatePayloadDto
    client_identifier: str


# Output

class TransferticketAndIdnrResponseDto(BaseDto):
    transferticket: str
    tax_id_number: str


class ResultFreischaltcodeRequestAndActivationDto(TransferticketAndIdnrResponseDto):
    elster_request_id: str


class FreischaltcodeRequestAndActivationResponseDto(ResponseBaseDto):
    result: Optional[ResultFreischaltcodeRequestAndActivationDto]


class FreischaltcodeRevocationResponseDto(ResponseBaseDto):
    result: Optional[TransferticketAndIdnrResponseDto]
