import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import EstDataWithElsterResponseAndTtl

router = APIRouter()


@router.post('/est_validations', status_code=status.HTTP_201_CREATED)
def validate_est(est_elsterresponse_ttl: EstDataWithElsterResponseAndTtl):
    """
    Route for validation of a tax declaration using the job queue.
    :param est_elsterresponse_ttl: payload with TTL, JSON input data for the ESt and declaration year.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not validate est", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.post('/ests', status_code=status.HTTP_201_CREATED)
def send_est(est_elsterresponse_ttl: EstDataWithElsterResponseAndTtl):
    """
    Route for sending a tax declaration using the job queue.
    :param est_elsterresponse_ttl: payload with TTL, JSON input data for the ESt, declaration year and option
    whether return the ERiC/Server response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not send est", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())
