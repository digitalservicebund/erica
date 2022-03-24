from datetime import date

from pydantic import BaseModel

from erica.application.base_dto import BaseDto


class FreischaltCodeRequestDto(BaseDto):
    idnr: str
    dob: date


class FreischaltCodeRequestWithClientIdentifier(BaseModel):
    payload: FreischaltCodeRequestDto
    clientIdentifier: str


class FreischaltCodeRevocateDto(BaseDto):
    idnr: str
    elster_request_id: str


class FreischaltCodeRevocationWithClientIdentifier(BaseModel):
    payload: FreischaltCodeRevocateDto
    clientIdentifier: str


class FreischaltCodeActivateDto(BaseDto):
    idnr: str
    unlock_code: str
    elster_request_id: str


class FreischaltCodeActiveWithClientIdentifier(BaseModel):
    payload: FreischaltCodeActivateDto
    clientIdentifier: str
