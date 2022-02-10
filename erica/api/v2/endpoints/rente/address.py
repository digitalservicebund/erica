import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import AddressWithTtl

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def get_address(address_ttl: AddressWithTtl):
    """
    Route for requesting the address data of a given id_rn using the job queue.
    :param address_ttl: payload with the JSON input data for the request and the option whether return the ERiC/Server
    response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve address data", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())
