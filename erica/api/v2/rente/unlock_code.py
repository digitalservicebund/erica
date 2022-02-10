import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import UnlockCodeRequestDataWithElsterResponseAndTtl, \
    UnlockCodeActivationDataWithElsterResponseAndTtl, UnlockCodeRevocationDataWithElsterResponseAndTtl

router = APIRouter()


@router.post('/unlock_code_requests', status_code=status.HTTP_201_CREATED)
def request_unlock_code(unlockCodeRequestDataWithElsterResponseAndTtl: UnlockCodeRequestDataWithElsterResponseAndTtl):
    """
    Route for requesting a new unlock code for the sent id_nr using the job queue.
    :param unlockCodeRequestDataWithElsterResponseAndTtl: payload with TTL, the JSON input data for the request and option
    whether return the ERiC/Server response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.post('/unlock_code_activations', status_code=status.HTTP_201_CREATED)
def activate_unlock_code(
        unlockCodeActivationDataWithElsterResponseAndTtl: UnlockCodeActivationDataWithElsterResponseAndTtl):
    """
    Route for requesting activation of an unlock code for the sent id_nr using the job queue.
    :param unlockCodeActivationDataWithElsterResponseAndTtl: payload with TTL, the JSON input data for the activation and option
    whether return the ERiC/Server response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.post('/unlock_code_revocations', status_code=status.HTTP_201_CREATED)
def revoke_unlock_code(
        unlockCodeRevocationDataWithElsterResponseAndTtl: UnlockCodeRevocationDataWithElsterResponseAndTtl):
    """
    Route for requesting revocation of an unlock code for the sent id_nr using the job queue.
    :param unlockCodeRevocationDataWithElsterResponseAndTtl: payload with TTL, the JSON input data for the revocation and option
    whether return the ERiC/Server response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())
