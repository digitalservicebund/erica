from opyoid import Module, Injector

from src.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface
from src.infrastructure.sqlalchemy.freischalt_code import FreischaltCodeEntity
from src.infrastructure.sqlalchemy.repositories.freischalt_code_activate_repository import \
    FreischaltCodeActivateRepository
from src.infrastructure.sqlalchemy.repositories.freischalt_code_repository import FreischaltCodeRepository


class RepositoriesModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeRepository)
        self.bind(BaseRepositoryInterface[FreischaltCodeEntity], to_class=FreischaltCodeActivateRepository)
