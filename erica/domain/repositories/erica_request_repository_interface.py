from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from erica.domain.Repositories.base_repository_interface import BaseRepositoryInterface
from erica.domain.erica_request.erica_request import EricaRequest


class EricaRequestRepositoryInterface(BaseRepositoryInterface[EricaRequest], ABC):

    @abstractmethod
    def get_by_job_id(self, job_id: UUID) -> EricaRequest:
        pass

    @abstractmethod
    def _get_by_job_id(self, job_id: UUID):
        pass

    @abstractmethod
    def update_by_job_id(self, job_id: UUID, model: BaseModel) -> EricaRequest:
        pass

    @abstractmethod
    def delete_by_job_id(self, job_id: UUID):
        pass
