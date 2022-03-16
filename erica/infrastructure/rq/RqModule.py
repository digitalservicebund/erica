from opyoid import Module

from erica.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from erica.infrastructure.rq.BackgroundJobRq import BackgroundJobRq


class RqModule(Module):
    def configure(self) -> None:
        self.bind(BackgroundJobInterface, to_class=BackgroundJobRq)
