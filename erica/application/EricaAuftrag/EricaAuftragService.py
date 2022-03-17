from abc import abstractmethod, ABCMeta
from uuid import UUID

from opyoid import Injector, Module

from erica.infrastructure.InfrastructureModule import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository

injector = Injector([InfrastructureModule(), RqModule()])


class EricaAuftragServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_status(self, auftrag_id: UUID):
        pass


class EricaAuftragService(EricaAuftragServiceInterface):
    erica_auftrag_repository: EricaAuftragRepository

    def __init__(self, repository: EricaAuftragRepository = injector.inject(EricaAuftragRepository)) -> None:
        super().__init__()
        self.erica_auftrag_repository = repository

    def get_status(self, auftrag_id: UUID):
        return self.erica_auftrag_repository.get_by_id(auftrag_id)


class EricaAuftragServiceModule(Module):
    def configure(self) -> None:
        self.bind(EricaAuftragServiceInterface, to_class=EricaAuftragService)