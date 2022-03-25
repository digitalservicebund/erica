from abc import ABC
from datetime import date

from erica.domain.Shared.BaseDomainModel import BasePayload


class FreischaltCodeRequestPayload(BasePayload, ABC):
    idnr: str
    dob: date


class FreischaltCodeActivatePayload(BasePayload, ABC):
    idnr: str
    unlock_code: str
    elster_request_id: str


class FreischaltCodeRevocatePayload(BasePayload, ABC):
    idnr: str
    elster_request_id: str