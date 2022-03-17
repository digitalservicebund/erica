from opyoid import Module

from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface, EricaAuftragService
from erica.application.FreischaltCode.FreischaltCodeActivationService import FreischaltCodeActivationServiceInterface, FreischaltCodeActivationService
from erica.application.FreischaltCode.FreischaltCodeRequestService import FreischaltCodeRequestService, FreischaltCodeRequestServiceInterface
from erica.infrastructure.InfrastructureModule import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule


class ApplicationModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeRequestServiceInterface, to_class=FreischaltCodeRequestService)
        self.bind(FreischaltCodeActivationServiceInterface, to_class=FreischaltCodeActivationService)
        self.bind(EricaAuftragServiceInterface, to_class=EricaAuftragService)
        self.install(InfrastructureModule())
        self.install(RqModule())
