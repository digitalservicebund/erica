from erica.application.base_dto import BaseDto
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeRequestPayload, FreischaltCodeActivatePayload, \
    FreischaltCodeRevocatePayload


class FreischaltCodeRequestDto(BaseDto):
    ttlInMinutes: int
    payload: FreischaltCodeRequestPayload


class FreischaltCodeActivateDto(BaseDto):
    ttlInMinutes: int
    payload: FreischaltCodeActivatePayload


class FreischaltCodeRevocateDto(BaseDto):
    ttlInMinutes: int
    payload: FreischaltCodeRevocatePayload
