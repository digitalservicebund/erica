import logging

from uuid import UUID
from fastapi import status, APIRouter
from opyoid import Injector
from starlette.responses import JSONResponse
from erica.api.ApiModule import ApiModule
from erica.api.utils import map_status, generate_error_response
from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface
from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeRequestWithClientIdentifier, \
    FreischaltCodeActiveWithClientIdentifier, FreischaltCodeRevocationWithClientIdentifier
from erica.api.v2.responses.model import response_model_get_unlock_code_request_from_queue, \
    response_model_get_unlock_code_activation_from_queue, response_model_get_unlock_code_revocation_from_queue, \
    ErrorRequestQueue, ResultGetUnlockCodeRequestAndActivationFromQueue, \
    SuccessResponseGetUnlockCodeRequestAndActivationFromQueue, JobState
from erica.application.JobService.job_service_factory import get_job_service
from erica.domain.Shared.EricaAuftrag import RequestType

router = APIRouter()

injector = Injector([
    ApiModule(),
])


@router.post('/request', status_code=status.HTTP_201_CREATED,
             responses={422: {"model": ErrorRequestQueue}, 500: {"model": ErrorRequestQueue}})
async def request_fsc(request_fsc_client_identifier: FreischaltCodeRequestWithClientIdentifier):
    """
    Route for requesting a new fsc for the sent id_nr using the job queue.
    :param request_fsc_client_identifier: payload with client identifier and the JSON input data for the request.
    """
    try:
        result = get_job_service(RequestType.freischalt_code_request).add_to_queue(
            request_fsc_client_identifier.payload, request_fsc_client_identifier.clientIdentifier,
            RequestType.freischalt_code_request)
        return 'request/' + str(result.job_id)
    # TODO specific exception?
    except Exception:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_error_response())


@router.get('/request/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_request_from_queue)
async def get_request_fsc_job(request_id: UUID):
    """
    Route for retrieving job status from an fsc request from the queue.
    :param request_id: the id of the job.
    """
    try:
        return get_request_and_activate_job_status(request_id)
    # TODO specific exception and correct mapping to JSON error response?
    except Exception as e:
        logging.getLogger().info("Could not retrieve status of (unlock code request) job " + str(request_id),
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_error_response(-1, e.__doc__))


@router.post('/activation', status_code=status.HTTP_201_CREATED,
             responses={422: {"model": ErrorRequestQueue}, 500: {"model": ErrorRequestQueue}})
async def activate_fsc(activation_fsc_client_identifier: FreischaltCodeActiveWithClientIdentifier):
    """
    Route for requesting activation of an fsc for the sent id_nr using the job queue.
    :param activation_fsc_client_identifier: payload with client identifier and the JSON input data for the activation.
    """
    try:
        result = get_job_service(RequestType.freischalt_code_activate).add_to_queue(
            activation_fsc_client_identifier.payload, activation_fsc_client_identifier.clientIdentifier,
            RequestType.freischalt_code_activate)
        return 'request/' + str(result.job_id)
    # TODO specific exception?
    except Exception:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_error_response())


@router.get('/activation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_activation_from_queue)
async def get_fsc_activation_job(request_id: UUID):
    """
    Route for retrieving job status from an fsc activation from the queue.
    :param request_id: the id of the job.
    """
    try:
        return get_request_and_activate_job_status(request_id)
    # TODO specific exception and correct mapping to JSON error response?
    except Exception as e:
        logging.getLogger().info("Could not retrieve status of (unlock code activation) job " + str(request_id),
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_error_response(-1, e.__doc__))


@router.post('/revocation', status_code=status.HTTP_201_CREATED, responses={422: {"model": ErrorRequestQueue}})
async def fsc_revocation(revocation_fsc_client_identifier: FreischaltCodeRevocationWithClientIdentifier):
    """
    Route for requesting revocation of an fsc for the sent id_nr using the job queue.
    :param revocation_fsc_client_identifier: payload with client identifier and the JSON input data for the revocation.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        return JSONResponse(status_code=422, content=generate_error_response())


@router.get('/revocation/{request_id}', status_code=status.HTTP_200_OK,
            responses=response_model_get_unlock_code_revocation_from_queue)
async def get_fsc_revocation_job(request_id: str):
    """
    Route for retrieving job status from an fsc revocation from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of (unlock code revocation) job " + request_id,
                                 exc_info=True)
        return JSONResponse(status_code=500, content=generate_error_response())


def get_request_and_activate_job_status(request_id: UUID):
    erica_request = get_erica_request(request_id)
    process_status = map_status(erica_request.status)
    if process_status == JobState.SUCCESS:
        result = ResultGetUnlockCodeRequestAndActivationFromQueue(
            elster_request_id=erica_request.result["elster_request_id"],
            transfer_ticket=erica_request.result["transfer_ticket"],
            idnr=erica_request.payload.get("idnr"))
        return SuccessResponseGetUnlockCodeRequestAndActivationFromQueue(
            processStatus=map_status(erica_request.status), result=result)
    elif process_status == JobState.FAILURE:
        return SuccessResponseGetUnlockCodeRequestAndActivationFromQueue(
            processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
            errorMessage=erica_request.error_message)
    else:
        return SuccessResponseGetUnlockCodeRequestAndActivationFromQueue(
            processStatus=map_status(erica_request.status))


def get_erica_request(job_id: UUID):
    freischalt_code_service: EricaAuftragServiceInterface = injector.inject(EricaAuftragServiceInterface)
    return freischalt_code_service.get_status(job_id)
