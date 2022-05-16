from uuid import UUID
from fastapi import status, APIRouter
from starlette.requests import Request
from starlette.responses import FileResponse, RedirectResponse
from erica.api.v2.responses.model import response_model_get_tax_number_validity_from_queue, response_model_post_to_queue
from erica.application.JobService.job_service_factory import get_job_service
from erica.application.Shared.service_injector import get_service
from erica.application.tax_number_validation.TaxNumberValidityService import TaxNumberValidityServiceInterface
from erica.application.tax_number_validation.check_tax_number_dto import CheckTaxNumberDto
from erica.domain.Shared.EricaRequest import RequestType

router = APIRouter()


@router.post('/tax_number_validity', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def is_valid_tax_number(tax_validity_client_identifier: CheckTaxNumberDto, request: Request):
    """
    Route for validation of a tax number using the job queue.
    :param request: API request object.
    :param tax_validity_client_identifier: payload with client identifier and the JSON input data for the tax number validity check.
    """
    result = get_job_service(RequestType.check_tax_number).add_to_queue(
        tax_validity_client_identifier.payload, tax_validity_client_identifier.client_identifier,
        RequestType.check_tax_number)
    return RedirectResponse(
        request.url_for("get_valid_tax_number_job", request_id=str(result.request_id)).removeprefix(str(request.base_url)),
        status_code=201)


@router.get('/tax_number_validity/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_tax_number_validity_from_queue)
async def get_valid_tax_number_job(request_id: UUID):
    """
    Route for retrieving job status of a tax number validity from the queue.
    :param request_id: the id of the job.
    """
    tax_number_validity_service: TaxNumberValidityServiceInterface = get_service(RequestType.check_tax_number)
    return tax_number_validity_service.get_response_tax_number_validity(request_id)


@router.get('/tax_offices/', status_code=status.HTTP_200_OK)
def get_tax_offices():
    """
    The list of tax offices for all states is requested and returned.
    """
    return FileResponse("erica/infrastructure/static/tax_offices.json")
