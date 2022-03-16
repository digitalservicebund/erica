from opyoid import Module

from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface, EricaAuftragService
from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeService, FreischaltCodeServiceInterface
from erica.infrastructure.infrastructure_module import InfrastructureModule


class ApplicationModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
        self.bind(EricaAuftragServiceInterface, to_class=EricaAuftragService)
        self.install(InfrastructureModule())
