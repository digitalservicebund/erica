from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from erica.domain.model.erica_request import EricaRequest
from erica.domain.repositories.base_repository_interface import BaseRepositoryInterface


class EricaRequestRepositoryInterface(BaseRepositoryInterface[EricaRequest], ABC):

    @abstractmethod
    def get_by_job_request_id(self, request_id: UUID) -> EricaRequest:
        pass

    @abstractmethod
    def _get_by_job_request_id(self, request_id: UUID):
        pass

    @abstractmethod
    def update_by_job_request_id(self, request_id: UUID, model: BaseModel) -> EricaRequest:
        pass

    @abstractmethod
    def delete_by_job_request_id(self, request_id: UUID):
        pass
