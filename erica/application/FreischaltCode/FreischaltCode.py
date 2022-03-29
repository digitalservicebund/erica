from typing import Optional

from erica.application.Shared.response_dto import ResponseBaseDto
from erica.application.base_dto import BaseDto
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeRequestPayload, FreischaltCodeRevocatePayload, \
    FreischaltCodeActivatePayload


# Input

class FreischaltCodeRequestDto(BaseDto):
    payload: FreischaltCodeRequestPayload
    clientIdentifier: str


class FreischaltCodeActivateDto(BaseDto):
    payload: FreischaltCodeActivatePayload
    clientIdentifier: str


class FreischaltCodeRevocateDto(BaseDto):
    payload: FreischaltCodeRevocatePayload
    clientIdentifier: str


# Output

class TransferTicketAndIdnr(BaseDto):
    transfer_ticket: str
    idnr: str


class ResultFreischaltcodeRequestAndActivation(TransferTicketAndIdnr):
    elster_request_id: str


class FreischaltcodeRequestAndActivationResponseDto(ResponseBaseDto):
    result: Optional[ResultFreischaltcodeRequestAndActivation]


class FreischaltcodeRevocationResponseDto(ResponseBaseDto):
    result: Optional[TransferTicketAndIdnr]
