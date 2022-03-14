from opyoid import Module

from erica.application.ApplicationModule import ApplicationModule


class ApiModule(Module):
    def configure(self) -> None:
        self.install(ApplicationModule())
