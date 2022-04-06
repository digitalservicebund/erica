import logging
from uuid import UUID
from fastapi import status, APIRouter
from starlette.responses import JSONResponse, RedirectResponse
from erica.api.utils import generate_error_response, get_entity_not_found_log_message
from erica.api.v2.responses.model import response_model_get_send_est_from_queue, response_model_post_to_queue
from erica.application.JobService.job_service_factory import get_job_service
from erica.application.Shared.service_injector import get_service
from erica.application.tax_declaration.TaxDeclarationService import TaxDeclarationServiceInterface
from erica.application.tax_declaration.tax_declaration_dto import TaxDeclarationDto
from erica.domain.Shared.EricaRequest import RequestType
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError

router = APIRouter()


@router.post('/ests', status_code=status.HTTP_201_CREATED, responses=response_model_post_to_queue)
async def send_est(est_data_client_identifier: TaxDeclarationDto):
    """
    Route for sending a tax declaration using the job queue.
    :param est_data_client_identifier: payload with client identifier and the JSON input data for the tax declaration.
    """
    try:
        result = get_job_service(RequestType.send_est).add_to_queue(
            est_data_client_identifier.payload, est_data_client_identifier.clientIdentifier,
            RequestType.send_est)
        return RedirectResponse(url='ests/' + str(result.request_id), status_code=201)
    except Exception:
        logging.getLogger().info("Could not send est", exc_info=True)
        return JSONResponse(status_code=422, content=generate_error_response())


@router.get('/ests/{request_id}', status_code=status.HTTP_200_OK, responses=response_model_get_send_est_from_queue)
async def get_send_est_job(request_id: UUID):
    """
    Route for retrieving job status of a sent tax declaration from the queue.
    :param request_id: the id of the job.
    """
    try:
        tax_declaration_service: TaxDeclarationServiceInterface = get_service(RequestType.send_est)
        return tax_declaration_service.get_response_send_est(request_id)
    except EntityNotFoundError as e:
        logging.getLogger().info(get_entity_not_found_log_message(request_id), exc_info=True)
        return JSONResponse(status_code=404, content=generate_error_response(-1, e.__doc__))
    except Exception as e:
        logging.getLogger().info("Could not retrieve status of (send tax declaration) job " + str(request_id),
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_error_response(-1, e.__doc__))
