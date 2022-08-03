from opyoid import Injector

from erica.application.application_module import ApplicationModule
from erica.application.freischaltcode.freischaltcode_service import FreischaltCodeServiceInterface
from erica.application.shared.base_service import BaseService
from erica.application.grundsteuer.grundsteuer_service import GrundsteuerServiceInterface
from erica.application.tax_declaration.tax_declaration_service import TaxDeclarationServiceInterface
from erica.application.tax_number_validation.tax_number_validition_service import TaxNumberValidityServiceInterface
from erica.domain.shared.erica_request import RequestType


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
