from typing import Callable, Type
from opyoid import Injector

from erica.job_service.application_module import ApplicationModule
from erica.worker.jobs.freischaltcode_jobs import activate_freischalt_code, request_freischalt_code, \
    revocate_freischalt_code
from erica.job_service.job_service import JobService, JobServiceInterface
from erica.worker.request_processing.grundsteuer_request_controller import GrundsteuerRequestController
from erica.api.dto.grundsteuer_dto import GrundsteuerPayload
from erica.worker.jobs.grundsteuer_jobs import send_grundsteuer
from erica.worker.jobs.tax_declaration_jobs import send_est
from erica.domain.payload.freischaltcode import FreischaltCodeRevocatePayload, FreischaltCodeActivatePayload, \
    FreischaltCodeRequestPayload
from erica.domain.model.base_domain_model import BasePayload
from erica.worker.jobs.tax_number_validation_jobs import check_tax_number
from erica.domain.model.erica_request import RequestType
from erica.domain.payload.tax_declaration import TaxDeclarationPayload
from erica.domain.payload.tax_number_validation import CheckTaxNumberPayload
from erica.worker.request_processing.requests_controller import UnlockCodeRequestController, \
    UnlockCodeActivationRequestController, UnlockCodeRevocationRequestController, EricaRequestController, \
    CheckTaxNumberRequestController, EstRequestController


def _freischalt_code_request_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRequestController)
    module.bind(Type[BasePayload], to_instance=FreischaltCodeRequestPayload)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=request_freischalt_code)

    return Injector([
        module
    ])


def _freischalt_code_activation_injector() :
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeActivationRequestController)
    module.bind(Type[BasePayload], to_instance=FreischaltCodeActivatePayload)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=activate_freischalt_code)

    return Injector([
        module
    ])


def _freischalt_code_revocation_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=UnlockCodeRevocationRequestController)
    module.bind(Type[BasePayload], to_instance=FreischaltCodeRevocatePayload)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=revocate_freischalt_code)

    return Injector([
        module
    ])


def _check_tax_number_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=CheckTaxNumberRequestController)
    module.bind(Type[BasePayload], to_instance=CheckTaxNumberPayload)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=check_tax_number)

    return Injector([
        module
    ])


def _send_est_injector():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=EstRequestController)
    module.bind(Type[BasePayload], to_instance=TaxDeclarationPayload)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=send_est)

    return Injector([
        module
    ])

def _send_grundsteuer():
    module = ApplicationModule()
    module.bind(Type[EricaRequestController], to_instance=GrundsteuerRequestController)
    module.bind(Type[BasePayload], to_instance=GrundsteuerPayload)
    module.bind(JobServiceInterface, to_class=JobService)
    module.bind(Callable, to_instance=send_grundsteuer)

    return Injector([
        module
    ])

# Register injector
injectors = {
    RequestType.freischalt_code_request: _freischalt_code_request_injector,
    RequestType.freischalt_code_activate: _freischalt_code_activation_injector,
    RequestType.freischalt_code_revocate: _freischalt_code_revocation_injector,
    RequestType.check_tax_number: _check_tax_number_injector,
    RequestType.send_est: _send_est_injector,
    RequestType.grundsteuer: _send_grundsteuer,
}


def get_job_service(request_type: RequestType) -> JobServiceInterface:
    """
    This is a factory to get a corretly wired job service. Use that function to get any JobServiceInterface instance.

    :param request_type: The request type. The JobServiceInterface is chosen and wired based on this type.
    :return: Correctly wired JobServiceInterface
    """
    injector = injectors.get(request_type)
    if not injector:
        raise NotImplementedError()

    return injector().inject(JobServiceInterface)

