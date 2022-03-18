import logging

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from erica.api.v2.responses.model import response_model_post_to_queue
from erica.erica_legacy.pyeric.utils import generate_dummy_error_response
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerWithTtl

router = APIRouter()


@router.post('/grundsteuer', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
def send_grundsteuer(grundsteuer_ttl: GrundsteuerWithTtl):
    """
    Route for sending a tax declaration using the job queue.
    :param grundsteuer_ttl: payload with TTL, JSON input data for the grundsteuer declaration.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not send est", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/grundsteuer/{request_id}', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
def get_grundsteuer(request_id: str):
    """
    Route for retrieving job status of a grundsteuer tax declaration validation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())
