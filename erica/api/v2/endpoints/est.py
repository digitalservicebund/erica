from uuid import UUID

from fastapi import status, APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from erica.api.v2.responses.model import response_model_get_send_est_from_queue, response_model_post_to_queue
from erica.application.JobService.job_service_factory import get_job_service
from erica.application.Shared.service_injector import get_service
from erica.application.tax_declaration.TaxDeclarationService import TaxDeclarationServiceInterface
from erica.application.tax_declaration.tax_declaration_dto import TaxDeclarationDto
from erica.domain.Shared.EricaRequest import RequestType

router = APIRouter()


@router.post('/ests', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def send_est(est_data_client_identifier: TaxDeclarationDto, request: Request):
    """
    Route for sending a tax declaration using the job queue.
    :param request: API request object.
    :param est_data_client_identifier: payload with client identifier and the JSON input data for the tax declaration.
    """
    result = get_job_service(RequestType.send_est).add_to_queue(
        est_data_client_identifier.payload, est_data_client_identifier.client_identifier,
        RequestType.send_est)
    return RedirectResponse(
        request.url_for("get_send_est_job", request_id=str(result.request_id)).removeprefix(str(request.base_url)),
        status_code=201)


@router.get('/ests/{request_id}', status_code=status.HTTP_200_OK, responses=response_model_get_send_est_from_queue)
async def get_send_est_job(request_id: UUID):
    """
    Route for retrieving job status of a sent tax declaration from the queue.
    :param request_id: the id of the job.
    """
    tax_declaration_service: TaxDeclarationServiceInterface = get_service(RequestType.send_est)
    return tax_declaration_service.get_response_send_est(request_id)
