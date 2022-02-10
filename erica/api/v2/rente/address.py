import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import AddressWithTtl

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def get_address(addressWithTtl: AddressWithTtl):
    """
    Route for requesting the address data of a given idrn using the job queue.
    :param addressWithTtl: payload with the JSON input data for the request and the option whether return the ERiC/Server response.
    """
    try:
        # For now, we do not allow data requests as we cannot guarantee that Elster already has the relevant data gathered
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve address data", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())
