from uuid import UUID

from opyoid import Injector

from erica.api.ApiModule import ApiModule
from erica.api.v2.responses.model import JobState
from erica.application.EricaRequest.EricaRequestService import EricaRequestServiceInterface
from erica.domain.Shared.Status import Status


def map_status(status: Status):
    """
    Mapper from internal rq job state to API job state.
            Parameters:
                    status (Status): the internal rq job state.
            Returns:
                    (JobState): the corresponding API job state.
    """
    switcher = {
        Status.new: JobState.PROCESSING,
        Status.scheduled: JobState.PROCESSING,
        Status.processing: JobState.PROCESSING,
        Status.failed: JobState.FAILURE,
        Status.success: JobState.SUCCESS
    }
    return switcher.get(status)


def generate_error_response(errorcode=-1, errormessage="API resource not yet implemented."):
    """
    Generator of error response for the API v2.
            Parameters:
                    errorcode (int): the error code number.
                    errormessage (str): the error message.
            Returns:
                    (dict): dict with error respones object.
    """
    error_response = {"errorCode": errorcode,
                      "errorMessage": errormessage
                      }
    return error_response


injector = Injector([
    ApiModule(),
])


def get_erica_request(request_id: UUID):
    freischalt_code_service: EricaRequestServiceInterface = injector.inject(EricaRequestServiceInterface)
    return freischalt_code_service.get_request(request_id)


def get_entity_not_found_log_message(request_id: UUID):
    return "Job with id " + str(request_id) + " not present in the queue."
