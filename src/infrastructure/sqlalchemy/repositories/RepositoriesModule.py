from opyoid import Module

from src.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface
from src.domain.Repositories.FreischaltCodeRepositoryInterface import FreischaltCodeRepositoryInterface
from src.infrastructure.sqlalchemy.FreischaltCodeSchema import FreischaltCodeSchema
from src.infrastructure.sqlalchemy.repositories.FreischaltCodeRepository import FreischaltCodeRepository


class RepositoriesModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeRepositoryInterface, to_class=FreischaltCodeRepository)
        self.bind(BaseRepositoryInterface[FreischaltCodeSchema], to_class=FreischaltCodeRepository)
