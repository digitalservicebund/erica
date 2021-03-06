from opyoid import Module

from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface, FreischaltCodeService
from erica.application.erica_request.erica_request_service import EricaRequestServiceInterface, EricaRequestService
from erica.application.grundsteuer.GrundsteuerService import GrundsteuerServiceInterface, GrundsteuerService
from erica.application.tax_declaration.TaxDeclarationService import TaxDeclarationServiceInterface, \
    TaxDeclarationService
from erica.application.tax_number_validation.TaxNumberValidityService import TaxNumberValidityServiceInterface, \
    TaxNumberValidityService
from erica.infrastructure.infrastructure_module import InfrastructureModule


class ApplicationModule(Module):
    def configure(self) -> None:
        self.bind(EricaRequestServiceInterface, to_class=EricaRequestService)
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
        self.bind(TaxDeclarationServiceInterface, to_class=TaxDeclarationService)
        self.bind(TaxNumberValidityServiceInterface, to_class=TaxNumberValidityService)
        self.bind(GrundsteuerServiceInterface, to_class=GrundsteuerService)
        self.install(InfrastructureModule())
