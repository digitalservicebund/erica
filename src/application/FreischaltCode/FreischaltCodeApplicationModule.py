from opyoid import Module

from src.application.FreischaltCode.freischalt_code_service import FreischaltCodeService


class FreischaltCodeApplicationModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeService)
