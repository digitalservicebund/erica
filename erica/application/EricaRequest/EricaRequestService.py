import logging

from abc import abstractmethod, ABCMeta
from uuid import UUID
from opyoid import Injector, Module
from erica.erica_legacy.config import get_settings
from erica.infrastructure.infrastructure_module import InfrastructureModule
from erica.infrastructure.rq.RqModule import RqModule
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository
from datetime import datetime

injector = Injector([InfrastructureModule(), RqModule()])


class EricaRequestServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_request_by_request_id(self, request_id: UUID):
        pass

    @abstractmethod
    def get_all_by_skip_and_limit(self, skip: int, limit: int):
        pass

    @abstractmethod
    def delete_success_fail_old_entities(self):
        pass

    @abstractmethod
    def set_processing_entities_to_failed(self):
        pass


class EricaRequestService(EricaRequestServiceInterface):
    erica_request_repository: EricaRequestRepository
    scheduler = None

    def __init__(self, repository: EricaRequestRepository) -> None:
        super().__init__()
        self.erica_request_repository = repository

    def get_request_by_request_id(self, request_id: UUID):
        return self.erica_request_repository.get_by_job_request_id(request_id)

    def get_all_by_skip_and_limit(self, skip: int, limit: int):
        return self.erica_request_repository.get(skip, limit)

    def delete_success_fail_old_entities(self):
        entities_deleted = self.erica_request_repository.delete_success_fail_old_entities(
            get_settings().ttl_success_fail_entities_in_min)
        logging.getLogger().debug(
            str(entities_deleted) + " success/fail entities deleted at " + datetime.now().strftime("%H:%M:%S"),
            exc_info=True)

    def set_processing_entities_to_failed(self):
        entities_updated = self.erica_request_repository.set_processing_entities_to_failed(
            get_settings().ttl_processing_entities_in_min)
        logging.getLogger().debug(
            str(entities_updated) + " processing entities  set to failedat " + datetime.now().strftime("%H:%M:%S"),
            exc_info=True)


class EricaRequestServiceModule(Module):
    def configure(self) -> None:
        self.bind(EricaRequestServiceInterface, to_class=EricaRequestService)
