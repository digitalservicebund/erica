import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.api.v2.responses.model import response_model_post_to_queue, response_model_get_from_queue
from erica.pyeric.utils import generate_dummy_error_response
from erica.request_processing.erica_input import EstDataWithTtl

router = APIRouter()


@router.post('/est_validations', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
def validate_est(est_data_ttl: EstDataWithTtl):
    """
    Route for validation of a tax declaration using the job queue.
    :param est_data_ttl: payload with TTL, JSON input data for the ESt and declaration year.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not validate est", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/est_validations/{request_id}', status_code=status.HTTP_200_OK, responses=response_model_get_from_queue)
def get_validate_est_job(request_id: str):
    """
    Route for retrieving job status of a tax declaration validation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/ests', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
def send_est(est_data_ttl: EstDataWithTtl):
    """
    Route for sending a tax declaration using the job queue.
    :param est_data_ttl: payload with TTL, JSON input data for the ESt and declaration year.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not send est", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/ests/{request_id}', status_code=status.HTTP_200_OK, responses=response_model_get_from_queue)
def get_send_est_job(request_id: str):
    """
    Route for retrieving job status of a sent tax declaration from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())
