import uuid

from fastapi import APIRouter
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from erica.api.dto.grundsteuer_dto import GrundsteuerDto
from erica.api.service.grundsteuer_service import GrundsteuerServiceInterface
from erica.api.service.service_injector import get_service
from erica.api.v2.responses.model import response_model_post_to_queue, response_model_get_send_grundsteuer_from_queue
from erica.domain.model.erica_request import RequestType
from erica.job_service.job_service_factory import get_job_service

router = APIRouter()


@router.post('/grundsteuer', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def send_grundsteuer(grundsteuer: GrundsteuerDto, request: Request):
    """
    Route for sending a grundsteuer tax declaration using the job queue.
    :param request: API request object.
    :param grundsteuer: payload with TTL, JSON input data for the grundsteuer declaration.
    """
    result = get_job_service(RequestType.grundsteuer).add_to_queue(
        grundsteuer.payload, grundsteuer.client_identifier, RequestType.grundsteuer)
    return RedirectResponse(
        str(request.url_for("get_grundsteuer_job", request_id=str(result.request_id))).removeprefix(str(request.base_url)),
        status_code=201)


@router.get('/grundsteuer/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_send_grundsteuer_from_queue)
async def get_grundsteuer_job(request_id: uuid.UUID):
    """
    Route for retrieving job status of a grundsteuer tax declaration validation from the queue.
    :param request_id: the id of the job.
    """
    grundsteuer_service: GrundsteuerServiceInterface = get_service(RequestType.grundsteuer)
    return grundsteuer_service.get_response_grundsteuer(request_id)
