import logging

from fastapi import HTTPException, status, APIRouter
from starlette.responses import FileResponse

from erica.application.tax_number_validation.check_tax_number_dto import CheckTaxNumberDto
from erica.domain.tax_number_validation.check_tax_number import StateAbbreviation
from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful
from erica.erica_legacy.request_processing.requests_controller import CheckTaxNumberRequestController

router = APIRouter()


@router.get('/tax_number_validity/{state_abbreviation}/{tax_number}', status_code=status.HTTP_200_OK)
def is_valid_tax_number(state_abbreviation: StateAbbreviation, tax_number: str):
    """
    Validates a tax number and returns the result

    :param state_abbreviation: Abbreviation of the state of the tax office
    :param tax_number: Tax number in the standard schema
    """
    try:
        input_data = CheckTaxNumberDto(state_abbreviation=state_abbreviation, tax_number=tax_number)
        return CheckTaxNumberRequestController(input_data).process()
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not validate tax number", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_responses=False))


@router.get('/tax_offices/', status_code=status.HTTP_200_OK)
def get_tax_offices():
    """
    The list of tax offices for all states is requested and returned.
    """
    return FileResponse("erica/erica_legacy/static/tax_offices.json")
