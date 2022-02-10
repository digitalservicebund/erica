import logging

from fastapi import status, APIRouter
from starlette.responses import FileResponse, JSONResponse
from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import TaxValidityWithTtl

router = APIRouter()


@router.post('/tax_number_validity', status_code=status.HTTP_201_CREATED)
def is_valid_tax_number(taxValidityWithTtl : TaxValidityWithTtl):
    """
    Route for validation of a tax number using the job queue.
    :param taxValidityWithTtl: payload with abbreviation of the state of the tax office and tax number in the standard schema.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not validate tax number", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/tax_offices/', status_code=status.HTTP_200_OK)
def get_tax_offices():
    """
    The list of tax offices for all states is requested and returned.
    """
    return FileResponse("erica/static/tax_offices.json")
