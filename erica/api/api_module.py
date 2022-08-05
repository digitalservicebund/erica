from opyoid import Module

from erica.job_service.application_module import ApplicationModule


class ApiModule(Module):
    def configure(self) -> None:
        self.install(ApplicationModule())
