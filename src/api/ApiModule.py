from opyoid import Module

from src.application.ApplicationModule import ApplicationModule


class ApiModule(Module):
    def configure(self) -> None:
        self.install(ApplicationModule())
