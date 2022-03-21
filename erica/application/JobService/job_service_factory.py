
from typing import Callable, Type

from opyoid import Injector
from erica.application.ApplicationModule import ApplicationModule
from erica.application.EricRequestProcessing.requests_controller import EricaRequestController, UnlockCodeActivationRequestController, UnlockCodeRequestController, UnlockCodeRevocationRequestController

from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto, FreischaltCodeRequestDto, FreischaltCodeRevocateDto
from erica.application.FreischaltCode.Jobs.jobs import activate_freischalt_code, request_freischalt_code, revocate_freischalt_code
from erica.application.JobService.job_service import JobService, JobServiceInterface
from erica.domain.Shared.EricaAuftrag import RequestType



def _freischalt_code_request_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRequestController)
    module.bind(Type[BaseDto], to_instance=FreischaltCodeRequestDto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=request_freischalt_code)

    return Injector([
        module
    ])

def _freischalt_code_activation_injector() :
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeActivationRequestController)
    module.bind(Type[BaseDto], to_instance=FreischaltCodeActivateDto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=activate_freischalt_code)
    
    return Injector([
        module
    ])

def _freischalt_code_revocation_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRevocationRequestController)
    module.bind(Type[BaseDto], to_instance=FreischaltCodeRevocateDto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=revocate_freischalt_code)

    return Injector([
        module
    ])

# Register injector
injectors = {
    RequestType.freischalt_code_request: _freischalt_code_request_injector,
    RequestType.freischalt_code_activate: _freischalt_code_activation_injector,
    RequestType.freischalt_code_revocate: _freischalt_code_revocation_injector,
}



def get_job_service(request_type: RequestType) -> JobServiceInterface:
    """
    This is a factory to get a corretly wired job service. Use that function to get any JobServiceInterface instance.

    :param request_type: The request type. The JobServiceInterface is chosen and wired based on this type.
    :param dto: Optional data transfer object; the input coming in through the API.
    :return: Correctly wired JobServiceInterface
    """
    injector = injectors.get(request_type)
    if not injector:
        raise NotImplementedError()

    return injector().inject(JobServiceInterface)

