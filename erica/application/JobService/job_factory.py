
from typing import Callable, Type

from opyoid import Injector
from erica.api.ApiModule import ApiModule
from erica.application.EricRequestProcessing.requests_controller import EricaRequestController, UnlockCodeActivationRequestController

from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto
from erica.application.FreischaltCode.Jobs.jobs import activate_freischalt_code
from erica.application.JobService.job_service import JobService, JobServiceInterface

injectors = []
    
def _freischalt_code_activation_injector(dto: FreischaltCodeActivateDto):
    _freischalt_code_activation_injector.handle_type = FreischaltCodeActivateDto
    
    module = ApiModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeActivationRequestController)
    module.bind(BaseDto, to_instance=dto)
    module.bind(object, to_instance=dto)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=activate_freischalt_code)
    
    return Injector([
        module
    ])

# Define handle types
_freischalt_code_activation_injector.handle_type = FreischaltCodeActivateDto

# Register injector
injectors.append(_freischalt_code_activation_injector)


def get_job(dto: BaseDto):
    for injector in injectors:
        if isinstance(dto, injector.handle_type):
            return injector(dto).inject(JobServiceInterface)
        
    raise NotImplementedError()