from opyoid import Module
from sqlalchemy.orm import Session

from src.domain.DomainModule import DomainModule
from src.domain.Repositories.BaseRepositoryInterface import BaseRepositoryInterface
from src.domain.Repositories.EricaAuftragRepositoryInterface import EricaAuftragRepositoryInterface
from src.infrastructure.sqlalchemy.EricaAuftragSchema import EricaAuftragSchema
from src.infrastructure.sqlalchemy.database import DatabaseSessionProvider
from src.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository


class InfrastructureModule(Module):
    def configure(self) -> None:
        self.install(DomainModule())
        self.bind(Session, to_provider=DatabaseSessionProvider)
        self.bind(EricaAuftragRepositoryInterface, to_class=EricaAuftragRepository)
        self.bind(BaseRepositoryInterface[EricaAuftragSchema], to_class=EricaAuftragRepository)
