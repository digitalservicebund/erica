from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic, Optional

from src.domain.audited_model import AuditedModel

DataT = TypeVar('DataT')
ClassT = TypeVar('ClassT')


class BaseDomainModel(AuditedModel, Generic[DataT]):
    id: Optional[DataT]


class BaseRepositoryInterface(Generic[ClassT]):
    __metaclass__ = ABCMeta
    entity: [ClassT]

    @abstractmethod
    def create(self, model: BaseDomainModel):
        pass

    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def get_by_id(self, entity_id):
        pass

    @abstractmethod
    def update(self, model_id, model: BaseDomainModel):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass
