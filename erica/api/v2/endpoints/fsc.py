import logging
from uuid import UUID

from fastapi import status, APIRouter
from opyoid import Injector
from starlette.responses import JSONResponse

from erica.api.ApiModule import ApiModule
from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface
from erica.application.FreischaltCode.FreischaltCode import FscRequestDataWithClientIdentifier
from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface
from erica.api.v2.responses.model import response_model_get_unlock_code_request_from_queue, \
    response_model_get_unlock_code_activation_from_queue, response_model_get_unlock_code_revocation_from_queue
from erica.erica_legacy.pyeric.utils import generate_dummy_error_response
from erica.erica_legacy.request_processing.erica_input.v2.erica_input import ErrorRequestQueue, \
    FscActivationDataWithTtl, FscRevocationDataWithTtl

router = APIRouter()

injector = Injector([
    ApiModule(),
])


@router.post('/request', status_code=status.HTTP_201_CREATED,
             responses={422: {"model": ErrorRequestQueue}, 500: {"model": ErrorRequestQueue}})
async def request_fsc(request_fsc_client_identifier: FscRequestDataWithClientIdentifier):
    """
    Route for requesting a new fsc for the sent id_nr using the job queue.
    :param request_fsc_client_identifier: payload with client identifier and the JSON input data for the request.
    """
    try:
        freischalt_code_service: FreischaltCodeServiceInterface = injector.inject(FreischaltCodeServiceInterface)
        result = await freischalt_code_service.freischalt_code_bei_elster_beantragen_queued(
            request_fsc_client_identifier.payload)
        return 'request/' + str(result.job_id)
    except Exception:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/request/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_request_from_queue)
def get_request_fsc_job(request_id: UUID):
    """
    Route for retrieving job status from an fsc request from the queue.
    :param request_id: the id of the job.
    """
    try:
        freischalt_code_service: EricaAuftragServiceInterface = injector.inject(EricaAuftragServiceInterface)
        return freischalt_code_service.get_status(request_id)
    except Exception:
        logging.getLogger().info("Could not retrieve status of (unlock code request) job " + str(request_id),
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/activation', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def activation_fsc(
        activation_fsc_ttl: FscActivationDataWithTtl):
    """
    Route for requesting activation of an fsc for the sent id_nr using the job queue.
    :param activation_fsc_ttl: payload with TTL and the JSON input data for the activation.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/activation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_activation_from_queue)
def get_fsc_activation_job(request_id: str):
    """
    Route for retrieving job status from an fsc activation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code activation) job " + request_id,
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())


@router.post('/revocation', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
def fsc_revocation(
        fsc_revocation_ttl: FscRevocationDataWithTtl):
    """
    Route for requesting revocation of an fsc for the sent id_nr using the job queue.
    :param fsc_revocation_ttl: payload with TTL and the JSON input data for the revocation.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_dummy_error_response())


@router.get('/revocation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_revocation_from_queue)
def get_fsc_revocation_job(request_id: str):
    """
    Route for retrieving job status from an fsc revocation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code revocation) job " + request_id,
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())
