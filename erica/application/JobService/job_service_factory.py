
from typing import Callable, Type

from opyoid import Injector
from erica.application.ApplicationModule import ApplicationModule
from erica.application.EricRequestProcessing.requests_controller import EricaRequestController, UnlockCodeActivationRequestController, UnlockCodeRequestController, UnlockCodeRevocationRequestController

from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto, FreischaltCodeRequestDto, FreischaltCodeRevocateDto
from erica.application.FreischaltCode.Jobs.jobs import activate_freischalt_code, request_freischalt_code, revocation_freischalt_code
from erica.application.JobService.job_service import JobService, JobServiceInterface
from erica.domain.Shared.EricaAuftrag import AuftragType



def _freischalt_code_request_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRequestController)
    module.bind(BaseDto, to_instance=FreischaltCodeRequestDto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=request_freischalt_code)

    return Injector([
        module
    ])

def _freischalt_code_activation_injector() :
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeActivationRequestController)
    module.bind(BaseDto, to_instance=FreischaltCodeActivateDto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=activate_freischalt_code)
    
    return Injector([
        module
    ])

def _freischalt_code_revocation_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRevocationRequestController)
    module.bind(BaseDto, to_instance=FreischaltCodeRevocateDto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=revocation_freischalt_code)

    return Injector([
        module
    ])

# Register injector
injectors = {
    AuftragType.freischalt_code_beantragen: _freischalt_code_request_injector
    AuftragType.freischalt_code_activate: _freischalt_code_activation_injector,
    AuftragType.freischalt_code_revocate: _freischalt_code_revocation_injector,
}



def get_job_service(request_type: AuftragType):
    injector = injectors.get(request_type)
    if not injector:
        raise NotImplementedError()

    return injector().inject(JobServiceInterface)

