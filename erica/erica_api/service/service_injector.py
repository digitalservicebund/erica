from opyoid import Injector

from erica.erica_shared.application_module import ApplicationModule
from erica.erica_api.service.freischaltcode_service import FreischaltCodeServiceInterface
from erica.erica_api.service.base_service import BaseService
from erica.erica_api.service.grundsteuer_service import GrundsteuerServiceInterface
from erica.erica_api.service.tax_declaration_service import TaxDeclarationServiceInterface
from erica.erica_api.service.tax_number_validition_service import TaxNumberValidityServiceInterface
from erica.erica_shared.model.erica_request import RequestType


def get_service(request_type: RequestType) -> BaseService:

    injector = Injector([
        ApplicationModule(),
    ])

    switcher = {
        RequestType.freischalt_code_request: injector.inject(FreischaltCodeServiceInterface),
        RequestType.freischalt_code_activate: injector.inject(FreischaltCodeServiceInterface),
        RequestType.freischalt_code_revocate: injector.inject(FreischaltCodeServiceInterface),
        RequestType.check_tax_number: injector.inject(TaxNumberValidityServiceInterface),
        RequestType.send_est: injector.inject(TaxDeclarationServiceInterface),
        RequestType.grundsteuer: injector.inject(GrundsteuerServiceInterface)
    }
    return switcher.get(request_type)
