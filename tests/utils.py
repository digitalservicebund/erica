import uuid
from datetime import date

from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeRequestWithClientIdentifier, \
    FreischaltCodeRequestDto, FreischaltCodeActiveWithClientIdentifier, FreischaltCodeActivateDto


def create_unlock_code_request(correct=True):
    if correct:
        payload = FreischaltCodeRequestDto(idnr="04531972802", dob=date(1957, 7, 14))
    else:
        payload = FreischaltCodeRequestDto(idnr="123456789", dob=date(1969, 7, 20))

    return FreischaltCodeRequestWithClientIdentifier(payload=payload, clientIdentifier="steuerlotse")


def create_unlock_code_activation(correct=True):
    if correct:
        payload = FreischaltCodeActivateDto(idnr="09952417688", unlock_code="42", elster_request_id="CORRECT")
    else:
        payload = FreischaltCodeActivateDto(idnr="123456789", unlock_code="INCORRECT", elster_request_id="INCORRECT")

    return FreischaltCodeActiveWithClientIdentifier(payload=payload, clientIdentifier="steuerlotse")


def json_default(value):
    if isinstance(value, date):
        return value.isoformat()
    else:
        return value.__dict__


def is_valid_uuid(value):
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def generate_uuid():
    return uuid.uuid4()
