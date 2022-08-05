from opyoid import Module
from sqlalchemy.orm import Session

from erica.domain.domain_module import DomainModule
from erica.domain.repositories.base_repository_interface import BaseRepositoryInterface
from erica.domain.repositories.erica_request_repository_interface import EricaRequestRepositoryInterface
from erica.domain.sqlalchemy.erica_request_schema import EricaRequestSchema
from erica.domain.sqlalchemy.database import DatabaseSessionProvider
from erica.domain.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


class InfrastructureModule(Module):
    def configure(self) -> None:
        self.install(DomainModule())
        self.bind(Session, to_provider=DatabaseSessionProvider)
        self.bind(EricaRequestRepositoryInterface, to_class=EricaRequestRepository)
        self.bind(BaseRepositoryInterface[EricaRequestSchema], to_class=EricaRequestRepository)
