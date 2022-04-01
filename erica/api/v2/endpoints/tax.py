from uuid import UUID

from fastapi import status, APIRouter
from starlette.responses import FileResponse, RedirectResponse

from erica.api.utils import get_erica_request, map_status
from erica.api.v2.responses.model import response_model_get_tax_number_validity_from_queue, ErrorRequestQueue, JobState, \
    TaxResponseDto, ResultGetTaxNumberValidityFromQueue
from erica.application.JobService.job_service_factory import get_job_service
from erica.application.tax_number_validation.check_tax_number_dto import CheckTaxNumberDto
from erica.domain.Shared.EricaRequest import RequestType

router = APIRouter()


@router.post('/tax_number_validity', status_code=status.HTTP_201_CREATED,
             responses={422: {"model": ErrorRequestQueue}, 500: {"model": ErrorRequestQueue}})
async def is_valid_tax_number(tax_validity_client_identifier: CheckTaxNumberDto):
    """
    Route for validation of a tax number using the job queue.
    :param tax_validity_client_identifier: payload with client identifier and the JSON input data for the tax number validity check.
    """
    result = get_job_service(RequestType.check_tax_number).add_to_queue(
        tax_validity_client_identifier.payload, tax_validity_client_identifier.clientIdentifier,
        RequestType.check_tax_number)
    return RedirectResponse(url='tax_number_validity/' + str(result.request_id), status_code=201)


@router.get('/tax_number_validity/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_tax_number_validity_from_queue)
async def get_valid_tax_number_job(request_id: UUID):
    """
    Route for retrieving job status of a tax number validity from the queue.
    :param request_id: the id of the job.
    """
    erica_request = get_erica_request(request_id)
    return create_response(erica_request)


@router.get('/tax_offices/', status_code=status.HTTP_200_OK)
def get_tax_offices():
    """
    The list of tax offices for all states is requested and returned.
    """
    return FileResponse("erica/infrastructure/static/tax_offices.json")


def create_response(erica_request):
    process_status = map_status(erica_request.status)
    if process_status == JobState.SUCCESS:
        result = ResultGetTaxNumberValidityFromQueue(
            is_valid=erica_request.result["is_valid"])
        return TaxResponseDto(
            processStatus=map_status(erica_request.status), result=result)
    elif process_status == JobState.FAILURE:
        return TaxResponseDto(
            processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
            errorMessage=erica_request.error_message)
    else:
        return TaxResponseDto(
            processStatus=map_status(erica_request.status))