from opyoid import Module

from erica.application.EricaRequest.EricaRequestService import EricaRequestServiceInterface, EricaRequestService
from erica.infrastructure.infrastructure_module import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule


class ApplicationModule(Module):
    def configure(self) -> None:
        self.bind(EricaRequestServiceInterface, to_class=EricaRequestService)
        self.install(InfrastructureModule())
        self.install(RqModule())
