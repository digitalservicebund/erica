import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import UnlockCodeRequestDataWithTtl, \
    UnlockCodeActivationDataWithTtl, UnlockCodeRevocationDataWithTtl, ErrorRequestQueue, ResponseGetFromQueue

router = APIRouter()


@router.post('/requests', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def request_unlock_code(unlock_code_request_ttl: UnlockCodeRequestDataWithTtl):
    """
    Route for requesting a new unlock code for the sent id_nr using the job queue.
    :param unlock_code_request_ttl: payload with TTL and the JSON input data for the request.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/requests/{request_id}', status_code=status.HTTP_200_OK, response_model=ResponseGetFromQueue,
            responses={500: {"model": ErrorRequestQueue}})
def get_unlock_code_request_job(request_id: str):
    """
    Route for retrieving job status from an unlock code request from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code request) job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/activations', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def activate_unlock_code(
        unlock_code_activation_ttl: UnlockCodeActivationDataWithTtl):
    """
    Route for requesting activation of an unlock code for the sent id_nr using the job queue.
    :param unlock_code_activation_ttl: payload with TTL and the JSON input data for the activation.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/activations/{request_id}', status_code=status.HTTP_200_OK, response_model=ResponseGetFromQueue,
            responses={500: {"model": ErrorRequestQueue}})
def get_unlock_code_activation_job(request_id: str):
    """
    Route for retrieving job status from an unlock code activation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code activation) job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/revocations', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def revoke_unlock_code(
        unlock_code_revocation_ttl: UnlockCodeRevocationDataWithTtl):
    """
    Route for requesting revocation of an unlock code for the sent id_nr using the job queue.
    :param unlock_code_revocation_ttl: payload with TTL and the JSON input data for the revocation.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/revocations/{request_id}', status_code=status.HTTP_200_OK, response_model=ResponseGetFromQueue,
            responses={500: {"model": ErrorRequestQueue}})
def get_unlock_code_revocation_job(request_id: str):
    """
    Route for retrieving job status from an unlock code revocation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code revocation) job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())
