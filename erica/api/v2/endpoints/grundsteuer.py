import logging
import uuid

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

from erica.api.utils import generate_error_response, get_entity_not_found_log_message
from erica.api.v2.responses.model import response_model_post_to_queue
from erica.application.JobService.job_service_factory import get_job_service
from erica.application.Shared.service_injector import get_service
from erica.application.grundsteuer.GrundsteuerService import GrundsteuerServiceInterface
from erica.application.grundsteuer.grundsteuer_dto import GrundsteuerDto
from erica.domain.Shared.EricaRequest import RequestType
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError

router = APIRouter()


@router.post('/grundsteuer', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def send_grundsteuer(grundsteuer: GrundsteuerDto):
    """
    Route for sending a grundsteuer tax declaration using the job queue.
    :param grundsteuer: payload with TTL, JSON input data for the grundsteuer declaration.
    """
    try:
        result = get_job_service(RequestType.grundsteuer).add_to_queue(
            grundsteuer.payload, grundsteuer.clientIdentifier, RequestType.grundsteuer)
        return RedirectResponse(url='grundsteuer/' + str(result.request_id), status_code=201)
    except Exception:
        logging.getLogger().info("Could not send grundsteuer", exc_info=True)
        return JSONResponse(status_code=422, content=generate_error_response())


@router.get('/grundsteuer/{request_id}', status_code=status.HTTP_200_OK, responses=response_model_post_to_queue)
async def get_grundsteuer_job(request_id: uuid.UUID):
    """
    Route for retrieving job status of a grundsteuer tax declaration validation from the queue.
    :param request_id: the id of the job.
    """
    try:
        grundsteuer_service: GrundsteuerServiceInterface = get_service(RequestType.grundsteuer)
        return grundsteuer_service.get_response_grundsteuer(request_id)
    except EntityNotFoundError as e:
        logging.getLogger().info(get_entity_not_found_log_message(request_id), exc_info=True)
        return JSONResponse(status_code=404, content=generate_error_response(-1, e.__doc__))
    except Exception as e:
        logging.getLogger().info("Could not retrieve status of (grundsteuer) job " + str(request_id),
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_error_response(-1, e.__doc__))
