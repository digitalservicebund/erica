from pydantic import BaseModel
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeRequestPayload, FreischaltCodeRevocatePayload, \
    FreischaltCodeActivatePayload


class FreischaltCodeRequestDto(BaseModel):
    payload: FreischaltCodeRequestPayload
    clientIdentifier: str


class FreischaltCodeActivateDto(BaseModel):
    payload: FreischaltCodeActivatePayload
    clientIdentifier: str


class FreischaltCodeRevocateDto(BaseModel):
    payload: FreischaltCodeRevocatePayload
    clientIdentifier: str
