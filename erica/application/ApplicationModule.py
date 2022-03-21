from opyoid import Module

from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface, EricaAuftragService
from erica.infrastructure.InfrastructureModule import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule


class ApplicationModule(Module):
    def configure(self) -> None:
        self.bind(EricaAuftragServiceInterface, to_class=EricaAuftragService)
        self.install(InfrastructureModule())
        self.install(RqModule())
