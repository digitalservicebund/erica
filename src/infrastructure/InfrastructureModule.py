from opyoid import Module
from sqlalchemy.orm import Session

from src.domain.DomainModule import DomainModule
from src.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface
from src.domain.Repositories.FreischaltCodeRepositoryInterface import FreischaltCodeRepositoryInterface
from src.infrastructure.sqlalchemy.FreischaltCodeSchema import FreischaltCodeSchema
from src.infrastructure.sqlalchemy.database import DatabaseSessionProvider
from src.infrastructure.sqlalchemy.repositories.FreischaltCodeRepository import FreischaltCodeRepository


class InfrastructureModule(Module):
    def configure(self) -> None:
        self.install(DomainModule())
        self.bind(Session, to_provider=DatabaseSessionProvider)
        self.bind(FreischaltCodeRepositoryInterface, to_class=FreischaltCodeRepository)
        self.bind(BaseRepositoryInterface[FreischaltCodeSchema], to_class=FreischaltCodeRepository)
