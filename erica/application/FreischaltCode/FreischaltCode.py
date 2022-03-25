from datetime import date

from erica.application.base_dto import BaseDto


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
