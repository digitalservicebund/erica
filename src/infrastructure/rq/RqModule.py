from opyoid import Module

from src.domain.BackgroundJobs.BackgroundJobInterface import BackgroundJobInterface
from src.infrastructure.rq.BackgroundJobRq import BackgroundJobRq


class RqModule(Module):
    def configure(self) -> None:
        self.bind(BackgroundJobInterface, to_class=BackgroundJobRq)
