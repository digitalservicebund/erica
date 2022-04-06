from opyoid import Injector

from erica.application.ApplicationModule import ApplicationModule
from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface
from erica.application.Shared.base_service import BaseService
from erica.application.grundsteuer.GrundsteuerService import GrundsteuerServiceInterface
from erica.application.tax_declaration.TaxDeclarationService import TaxDeclarationServiceInterface
from erica.application.tax_number_validation.TaxNumberValidityService import TaxNumberValidityServiceInterface
from erica.domain.Shared.EricaRequest import RequestType


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
