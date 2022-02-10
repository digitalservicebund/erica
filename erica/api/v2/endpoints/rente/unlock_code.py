import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import UnlockCodeRequestDataWithElsterResponseAndTtl, \
    UnlockCodeActivationDataWithElsterResponseAndTtl, UnlockCodeRevocationDataWithElsterResponseAndTtl

router = APIRouter()


@router.post('/unlock_code_requests', status_code=status.HTTP_201_CREATED)
def request_unlock_code(unlockcode_request_elsterresponse_ttl: UnlockCodeRequestDataWithElsterResponseAndTtl):
    """
    Route for requesting a new unlock code for the sent id_nr using the job queue.
    :param unlockcode_request_elsterresponse_ttl: payload with TTL, the JSON input data for the request and option
    whether return the ERiC/Server response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/unlock_code_requests/{request_id}', status_code=status.HTTP_200_OK)
def get_unlock_code_request_job(request_id: str):
    """
    Route for retrieving job status from an unlock code request from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/unlock_code_activations', status_code=status.HTTP_201_CREATED)
def activate_unlock_code(
        unlockcode_activation_elsterresponse_ttl: UnlockCodeActivationDataWithElsterResponseAndTtl):
    """
    Route for requesting activation of an unlock code for the sent id_nr using the job queue.
    :param unlockcode_activation_elsterresponse_ttl: payload with TTL, the JSON input data for the activation and option
    whether return the ERiC/Server response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/unlock_code_activations/{request_id}', status_code=status.HTTP_200_OK)
def get_unlock_code_activation_job(request_id: str):
    """
    Route for retrieving job status from an unlock code activation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/unlock_code_revocations', status_code=status.HTTP_201_CREATED)
def revoke_unlock_code(
        unlockcode_revocation_elsterresponse_ttl: UnlockCodeRevocationDataWithElsterResponseAndTtl):
    """
    Route for requesting revocation of an unlock code for the sent id_nr using the job queue.
    :param unlockcode_revocation_elsterresponse_ttl: payload with TTL, the JSON input data for the revocation and option
    whether return the ERiC/Server response.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/unlock_code_revocations/{request_id}', status_code=status.HTTP_200_OK)
def get_unlock_code_revocation_job(request_id: str):
    """
    Route for retrieving job status from an unlock code revocation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())
