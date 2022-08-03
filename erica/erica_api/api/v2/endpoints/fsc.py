from uuid import UUID

from fastapi import status, APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from erica.erica_api.api.v2.responses.model import response_model_get_unlock_code_request_from_queue, \
    response_model_get_unlock_code_activation_from_queue, response_model_get_unlock_code_revocation_from_queue, \
    response_model_post_to_queue
from erica.erica_api.dto.freischaltcode import FreischaltCodeRequestDto, FreischaltCodeActivateDto, \
    FreischaltCodeRevocateDto
from erica.erica_api.service.freischaltcode_service import FreischaltCodeService, FreischaltCodeServiceInterface
from erica.erica_shared.job_service.job_service_factory import get_job_service
from erica.erica_api.service.service_injector import get_service
from erica.erica_shared.model.erica_request import RequestType

router = APIRouter()


@router.post('/request', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def request_fsc(request_fsc_client_identifier: FreischaltCodeRequestDto, request: Request):
    """
    Route for requesting a new fsc for the sent id_nr using the job queue.
    :param request: API request object.
    :param request_fsc_client_identifier: payload with client identifier and the JSON input data for the request.
    """
    result = get_job_service(RequestType.freischalt_code_request).add_to_queue(
        request_fsc_client_identifier.payload, request_fsc_client_identifier.client_identifier,
        RequestType.freischalt_code_request)
    return RedirectResponse(
        request.url_for("get_fsc_request_job", request_id=str(result.request_id)).removeprefix(str(request.base_url)),
        status_code=201)


@router.get('/request/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_request_from_queue)
async def get_fsc_request_job(request_id: UUID):
    """
    Route for retrieving job status from an fsc request from the queue.
    :param request_id: the id of the job.
    """
    freischaltcode_service: FreischaltCodeServiceInterface = get_service(RequestType.freischalt_code_request)
    return freischaltcode_service.get_response_freischaltcode_request(request_id)


@router.post('/activation', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def activate_fsc(activation_fsc_client_identifier: FreischaltCodeActivateDto, request: Request):
    """
    Route for requesting activation of an fsc for the sent id_nr using the job queue.
    :param request: API request object.
    :param activation_fsc_client_identifier: payload with client identifier and the JSON input data for the activation.
    """
    result = get_job_service(RequestType.freischalt_code_activate).add_to_queue(
        activation_fsc_client_identifier.payload, activation_fsc_client_identifier.client_identifier,
        RequestType.freischalt_code_activate)
    return RedirectResponse(
        request.url_for("get_fsc_activation_job", request_id=str(result.request_id)).removeprefix(
            str(request.base_url)),
        status_code=201)


@router.get('/activation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_activation_from_queue)
async def get_fsc_activation_job(request_id: UUID):
    """
    Route for retrieving job status from an fsc activation from the queue.
    :param request_id: the id of the job.
    """
    freischaltcode_service: FreischaltCodeService = get_service(RequestType.freischalt_code_activate)
    return freischaltcode_service.get_response_freischaltcode_activation(request_id)


@router.post('/revocation', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def revocate_fsc(revocation_fsc_client_identifier: FreischaltCodeRevocateDto, request: Request):
    """
    Route for requesting revocation of an fsc for the sent id_nr using the job queue.
    :param request: API request object.
    :param revocation_fsc_client_identifier: payload with client identifier and the JSON input data for the revocation.
    """
    result = get_job_service(RequestType.freischalt_code_revocate).add_to_queue(
        revocation_fsc_client_identifier.payload, revocation_fsc_client_identifier.client_identifier,
        RequestType.freischalt_code_revocate)
    return RedirectResponse(
        request.url_for("get_fsc_revocation_job", request_id=str(result.request_id)).removeprefix(
            str(request.base_url)),
        status_code=201)


@router.get('/revocation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_revocation_from_queue)
async def get_fsc_revocation_job(request_id: UUID):
    """
    Route for retrieving job status from an fsc revocation from the queue.
    :param request_id: the id of the job.
    """
    freischaltcode_service: FreischaltCodeService = get_service(RequestType.freischalt_code_revocate)
    return freischaltcode_service.get_response_freischaltcode_revocation(request_id)
