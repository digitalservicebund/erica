from opyoid import Module

from erica.application.application_module import ApplicationModule


class ApiModule(Module):
    def configure(self) -> None:
        self.install(ApplicationModule())
