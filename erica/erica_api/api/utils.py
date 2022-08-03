from uuid import UUID

from opyoid import Injector

from erica.erica_api.api.api_module import ApiModule
from erica.application.shared.response_dto import JobState
from erica.application.erica_request.erica_request_service import EricaRequestServiceInterface
from erica.erica_shared.model.erica_request import Status


def map_status(status: Status):
    """
    Mapper from internal queue job state to API job state.
            Parameters:
                    status (Status): the internal queue job state.
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
    error_response = {"error_code": errorcode,
                      "error_message": errormessage
                      }
    return error_response


injector = Injector([
    ApiModule(),
])


def get_erica_request(request_id: UUID):
    erica_request_service: EricaRequestServiceInterface = injector.inject(EricaRequestServiceInterface)
    return erica_request_service.get_request_by_request_id(request_id)
