import uuid
from datetime import date

from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeRequestDto, FreischaltCodeActivateDto, FreischaltCodeRevocateDto
from erica.application.tax_declaration.tax_declaration_dto import  TaxDeclarationDto
from erica.application.tax_number_validation.check_tax_number_dto import CheckTaxNumberDto
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeRequestPayload, FreischaltCodeActivatePayload, \
    FreischaltCodeRevocatePayload
from erica.domain.TaxDeclaration.TaxDeclaration import TaxDeclarationPayload
from erica.domain.tax_number_validation.check_tax_number import CheckTaxNumberPayload
from tests.erica_legacy.utils import create_meta_data, create_form_data


def create_unlock_code_request(correct=True):
    if correct:
        payload = FreischaltCodeRequestPayload(idnr="04531972802", dob=date(1957, 7, 14))
    else:
        payload = FreischaltCodeRequestPayload(idnr="123456789", dob=date(1969, 7, 20))

    return FreischaltCodeRequestDto(payload=payload, clientIdentifier="steuerlotse")


def create_unlock_code_activation(correct=True):
    if correct:
        payload = FreischaltCodeActivatePayload(idnr="09952417688", unlock_code="42", elster_request_id="CORRECT")
    else:
        payload = FreischaltCodeActivatePayload(idnr="123456789", unlock_code="INCORRECT", elster_request_id="INCORRECT")

    return FreischaltCodeActivateDto(payload=payload, clientIdentifier="steuerlotse")


def create_unlock_code_revocation(correct=True):
    if correct:
        payload = FreischaltCodeRevocatePayload(idnr="04531972802", elster_request_id="CORRECT")
    else:
        payload = FreischaltCodeRevocatePayload(idnr="123456789", elster_request_id="INCORRECT")

    return FreischaltCodeRevocateDto(payload=payload, clientIdentifier="steuerlotse")


def create_tax_number_validity(correct=True):
    if correct:
        payload = CheckTaxNumberPayload(state_abbreviation="BY", tax_number="04531972802")
    else:
        payload = CheckTaxNumberPayload(state_abbreviation="BY", tax_number="123456789")

    return CheckTaxNumberDto(payload=payload, clientIdentifier="steuerlotse")


def create_send_est():
    payload = TaxDeclarationPayload(est_data=create_form_data(), meta_data=create_meta_data())
    return TaxDeclarationDto(payload=payload, clientIdentifier="steuerlotse")


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


def get_job_service_patch_string(endpoint):
    return "erica.api.v2.endpoints." + endpoint + ".get_job_service"
