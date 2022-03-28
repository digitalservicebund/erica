from abc import abstractmethod, ABCMeta
from uuid import UUID

from opyoid import Injector, Module

from erica.infrastructure.infrastructure_module import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository

injector = Injector([InfrastructureModule(), RqModule()])


class EricaRequestServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_status(self, auftrag_id: UUID):
        pass


class EricaRequestService(EricaRequestServiceInterface):
    erica_auftrag_repository: EricaRequestRepository

    def __init__(self, repository: EricaRequestRepository) -> None:
        super().__init__()
        self.erica_auftrag_repository = repository

    def get_status(self, request_id: UUID):
        return self.erica_auftrag_repository.get_by_job_request_id(request_id)


class EricaRequestServiceModule(Module):
    def configure(self) -> None:
        self.bind(EricaRequestServiceInterface, to_class=EricaRequestService)
