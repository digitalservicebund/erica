import logging
import uuid

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse, RedirectResponse

from erica.api.utils import map_status, generate_error_response, get_erica_request, get_entity_not_found_log_message
from erica.api.v2.responses.model import GrundsteuerResponseDto, ResultGrundsteuerFromQueue, response_model_post_to_queue, ErrorRequestQueue, ErrorRequestQueue, JobState
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerDto
from erica.application.JobService.job_service_factory import get_job_service
from erica.domain.Shared.EricaRequest import RequestType
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError

router = APIRouter()


@router.post('/request', status_code=status.HTTP_201_CREATED, responses={
        422: {"model": ErrorRequestQueue}, 500: {"model": ErrorRequestQueue}
    })
async def send_grundsteuer(grundsteuer_ttl: GrundsteuerDto):
    """
    Route for sending a grundsteuer tax declaration using the job queue.
    :param grundsteuer_ttl: payload with TTL, JSON input data for the grundsteuer declaration.
    """
    try:        
        result = get_job_service(RequestType.grundsteuer).add_to_queue(
            grundsteuer_ttl.payload, grundsteuer_ttl.clientIdentifier, RequestType.grundsteuer)
        return RedirectResponse(url='grundsteuer/request/' + str(result.request_id), status_code=201)
    except Exception as e:
        logging.getLogger().info("Could not send est", exc_info=True)
        return JSONResponse(status_code=422, content=generate_error_response())


@router.get('/request/{request_id}', status_code=status.HTTP_200_OK, responses=response_model_post_to_queue)
async def get_grundsteuer_job(request_id: uuid.UUID):
    """
    Route for retrieving job status of a grundsteuer tax declaration validation from the queue.
    :param request_id: the id of the job.
    """    
    try:
        erica_request = get_erica_request(request_id)
        return create_request_grundsteuer_response(erica_request)
    except EntityNotFoundError as e:
        logging.getLogger().info(get_entity_not_found_log_message(request_id), exc_info=True)
        return JSONResponse(status_code=404, content=generate_error_response(-1, e.__doc__))
    except Exception as e:
        logging.getLogger().info("Could not retrieve status of (grundsteuer) job " + str(request_id),
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_error_response(-1, e.__doc__))
    
def create_request_grundsteuer_response(erica_request):
    process_status = map_status(erica_request.status)
    if process_status == JobState.SUCCESS:
        result = ResultGrundsteuerFromQueue(
            transfer_ticket=erica_request.result["transfer_ticket"],
            pdf=erica_request.result["pdf"])
        return GrundsteuerResponseDto(
            processStatus=map_status(erica_request.status), result=result)
    elif process_status == JobState.FAILURE:
        return GrundsteuerResponseDto(
            processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
            errorMessage=erica_request.error_message)
    else:
        return GrundsteuerResponseDto(
            processStatus=map_status(erica_request.status))
