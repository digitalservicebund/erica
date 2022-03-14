from opyoid import Module
from sqlalchemy.orm import Session

from erica.domain.DomainModule import DomainModule
from erica.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface
from erica.domain.Repositories.EricaAuftragRepositoryInterface import EricaAuftragRepositoryInterface
from erica.infrastructure.sqlalchemy.EricaAuftragSchema import EricaAuftragSchema
from erica.infrastructure.sqlalchemy.database import DatabaseSessionProvider
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository


class InfrastructureModule(Module):
    def configure(self) -> None:
        self.install(DomainModule())
        self.bind(Session, to_provider=DatabaseSessionProvider)
        self.bind(EricaAuftragRepositoryInterface, to_class=EricaAuftragRepository)
        self.bind(BaseRepositoryInterface[EricaAuftragSchema], to_class=EricaAuftragRepository)
