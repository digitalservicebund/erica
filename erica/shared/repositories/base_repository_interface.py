from abc import ABCMeta, abstractmethod
from typing import Generic, List, TypeVar

from erica.shared.model.base_domain_model import BaseDomainModel

ClassT = TypeVar('ClassT', bound=BaseDomainModel)


class BaseRepositoryInterface(Generic[ClassT]):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, model: ClassT) -> ClassT:
        pass

    @abstractmethod
    def get(self) -> List[ClassT]:
        pass

    @abstractmethod
    def get_by_id(self, request_id) -> ClassT:
        pass

    @abstractmethod
    def update(self, model_id, model: ClassT) -> ClassT:
        pass

    @abstractmethod
    def delete(self, request_id) -> bool:
        pass


