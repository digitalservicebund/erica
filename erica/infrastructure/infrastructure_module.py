from opyoid import Module
from sqlalchemy.orm import Session

from erica.domain.DomainModule import DomainModule
from erica.domain.Repositories.base_repository_interface import BaseRepositoryInterface
from erica.domain.Repositories.erica_request_repository_interface import EricaRequestRepositoryInterface
from erica.infrastructure.sqlalchemy.erica_request_schema import EricaRequestSchema
from erica.infrastructure.sqlalchemy.database import DatabaseSessionProvider
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


class InfrastructureModule(Module):
    def configure(self) -> None:
        self.install(DomainModule())
        self.bind(Session, to_provider=DatabaseSessionProvider)
        self.bind(EricaRequestRepositoryInterface, to_class=EricaRequestRepository)
        self.bind(BaseRepositoryInterface[EricaRequestSchema], to_class=EricaRequestRepository)
