

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
    def get_request_by_request_id(self, request_id: UUID):
        pass

    @abstractmethod
    def get_all_by_skip_and_limit(self, skip: int, limit: int):
        pass


class EricaRequestService(EricaRequestServiceInterface):
    erica_request_repository: EricaRequestRepository

    def __init__(self, repository: EricaRequestRepository) -> None:
        super().__init__()
        self.erica_request_repository = repository

    def get_request_by_request_id(self, request_id: UUID):
        return self.erica_request_repository.get_by_job_request_id(request_id)

    def get_all_by_skip_and_limit(self, skip: int, limit: int):
        return self.erica_request_repository.get(skip, limit)


class EricaRequestServiceModule(Module):
    def configure(self) -> None:
        self.bind(EricaRequestServiceInterface, to_class=EricaRequestService)
