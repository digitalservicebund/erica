from opyoid import Module

from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeService, FreischaltCodeServiceInterface
from erica.infrastructure.InfrastructureModule import InfrastructureModule


class ApplicationModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
        self.install(InfrastructureModule())
