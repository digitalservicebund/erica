import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from src.erica_legacy.api.v2.responses.model import response_model_get_unlock_code_request_from_queue, \
    response_model_get_unlock_code_activation_from_queue, response_model_get_unlock_code_revocation_from_queue
from src.erica_legacy.pyeric.utils import generate_dummy_error_response
from src.erica_legacy.request_processing.erica_input.v2.erica_input import ErrorRequestQueue, FscRequestDataWithTtl, \
    FscActivationDataWithTtl, FscRevocationDataWithTtl

router = APIRouter()


@router.post('/request', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def request_fsc(request_fsc_ttl: FscRequestDataWithTtl):
    """
    Route for requesting a new fsc for the sent id_nr using the job queue.
    :param request_fsc_ttl: payload with TTL and the JSON input data for the request.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/request/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_request_from_queue)
def get_request_fsc_job(request_id: str):
    """
    Route for retrieving job status from an fsc request from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code request) job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/activation', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def activation_fsc(
        activation_fsc_ttl: FscActivationDataWithTtl):
    """
    Route for requesting activation of an fsc for the sent id_nr using the job queue.
    :param activation_fsc_ttl: payload with TTL and the JSON input data for the activation.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/activation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_activation_from_queue)
def get_fsc_activation_job(request_id: str):
    """
    Route for retrieving job status from an fsc activation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code activation) job " + request_id,
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/revocation', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def fsc_revocation(
        fsc_revocation_ttl: FscRevocationDataWithTtl):
    """
    Route for requesting revocation of an fsc for the sent id_nr using the job queue.
    :param fsc_revocation_ttl: payload with TTL and the JSON input data for the revocation.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/revocation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_revocation_from_queue)
def get_fsc_revocation_job(request_id: str):
    """
    Route for retrieving job status from an fsc revocation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code revocation) job " + request_id,
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())
