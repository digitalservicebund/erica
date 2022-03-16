from opyoid import Module
from sqlalchemy.orm import Session

from erica.domain.DomainModule import DomainModule
from erica.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface
from erica.domain.Repositories.EricaRequestRepositoryInterface import EricaRequestRepositoryInterface
from erica.infrastructure.sqlalchemy.EricaAuftragSchema import EricaAuftragSchema
from erica.infrastructure.sqlalchemy.database import DatabaseSessionProvider
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


class InfrastructureModule(Module):
    def configure(self) -> None:
        self.install(DomainModule())
        self.bind(Session, to_provider=DatabaseSessionProvider)
        self.bind(EricaRequestRepositoryInterface, to_class=EricaRequestRepository)
        self.bind(BaseRepositoryInterface[EricaAuftragSchema], to_class=EricaRequestRepository)
