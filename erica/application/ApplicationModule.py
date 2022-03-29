from opyoid import Module

from erica.application.EricaRequest.EricaRequestService import EricaRequestServiceInterface, EricaRequestService
from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface, FreischaltCodeService
from erica.application.tax_declaration.TaxDeclarationService import TaxDeclarationServiceInterface, \
    TaxDeclarationService
from erica.application.tax_number_validation.TaxNumberValidityService import TaxNumberValidityServiceInterface, \
    TaxNumberValidityService
from erica.infrastructure.infrastructure_module import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule


class ApplicationModule(Module):
    def configure(self) -> None:
        self.bind(EricaRequestServiceInterface, to_class=EricaRequestService)
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
        self.bind(TaxDeclarationServiceInterface, to_class=TaxDeclarationService)
        self.bind(TaxNumberValidityServiceInterface, to_class=TaxNumberValidityService)
        self.install(InfrastructureModule())
        self.install(RqModule())
