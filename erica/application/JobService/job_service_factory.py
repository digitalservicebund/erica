
from typing import Callable, Type

from opyoid import Injector
from erica.application.ApplicationModule import ApplicationModule
from erica.application.EricRequestProcessing.requests_controller import EricaRequestController, UnlockCodeActivationRequestController, UnlockCodeRequestController, UnlockCodeRevocationRequestController

from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto, FreischaltCodeRequestDto, FreischaltCodeRevocateDto
from erica.application.FreischaltCode.Jobs.jobs import activate_freischalt_code, request_freischalt_code, revocation_freischalt_code
from erica.application.JobService.job_service import JobService, JobServiceInterface


def _freischalt_code_activation_injector(dto: FreischaltCodeActivateDto):    
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeActivationRequestController)
    module.bind(BaseDto, to_instance=dto)
    module.bind(object, to_instance=dto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=activate_freischalt_code)
    
    return Injector([
        module
    ])
    
def _freischalt_code_revocation_injector(dto: FreischaltCodeRequestDto):    
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRevocationRequestController)
    module.bind(BaseDto, to_instance=dto)
    module.bind(object, to_instance=dto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=revocation_freischalt_code)
    
    return Injector([
        module
    ])
        
def _freischalt_code_request_injector(dto: FreischaltCodeRevocateDto):    
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRequestController)
    module.bind(BaseDto, to_instance=dto)
    module.bind(object, to_instance=dto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=request_freischalt_code)
    
    return Injector([
        module
    ])

# Register injector
injectors = {
    FreischaltCodeActivateDto : _freischalt_code_activation_injector,
    FreischaltCodeRequestDto : _freischalt_code_revocation_injector,
    FreischaltCodeRevocateDto: _freischalt_code_request_injector
}


def get_job_service(dto):
    injector = injectors.get(type(dto))
    
    if injector is None:
        raise NotImplementedError()
    
    return injector(dto).inject(JobServiceInterface)