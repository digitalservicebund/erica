from erica.application.base_dto import BaseDto
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeRequestPayload, FreischaltCodeActivatePayload, \
    FreischaltCodeRevocatePayload


class FreischaltCodeRequestDto(BaseDto):
    payload: FreischaltCodeRequestPayload
    clientIdentifier: str


class FreischaltCodeActivateDto(BaseDto):
    payload: FreischaltCodeActivatePayload
    clientIdentifier: str


class FreischaltCodeRevocateDto(BaseDto):
    payload: FreischaltCodeRevocatePayload
    clientIdentifier: str
