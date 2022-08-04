from opyoid import Module

from erica.shared.application_module import ApplicationModule


class ApiModule(Module):
    def configure(self) -> None:
        self.install(ApplicationModule())
