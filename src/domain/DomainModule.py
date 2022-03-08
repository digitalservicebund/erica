from opyoid import Module


class DomainModule(Module):
    def configure(self) -> None:
        pass
        # self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
