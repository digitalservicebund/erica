from datetime import date

from pydantic import BaseModel


class BaseDto(BaseModel):
    pass


class FreischaltCodeRequestDto(BaseDto):
    idnr: str
    date_of_birth: date


class FreischaltCodeRevocateDto(BaseDto):
    idnr: str
    elster_request_id: str


class FreischaltCodeActivateDto(BaseDto):
    idnr: str
    freischalt_code: str
    elster_request_id: str
