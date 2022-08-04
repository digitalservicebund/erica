from typing import Generic, TypeVar, List
from pydantic import BaseModel
from sqlalchemy import Integer
from sqlalchemy.orm import Session

from erica.shared.repositories.base_repository_interface import BaseRepositoryInterface
from erica.shared.model.base_domain_model import BaseDomainModel
from erica.shared.sqlalchemy.erica_request_schema import BaseDbSchema


class EntityNotFoundError(Exception):
    """Raised in case an entity could not be found in the database"""
    pass


T = TypeVar('T', bound=BaseDomainModel)
D = TypeVar('D', bound=BaseDbSchema)


class BaseRepository(BaseRepositoryInterface[T], Generic[T, D]):
    DatabaseEntity: D
    DomainModel: T
    db_connection: Session

    def __init__(self, db_connection: Session):
        self.db_connection = db_connection

    def create(self, model: BaseModel) -> T:
        new_entity = self.DatabaseEntity(**model.dict())
        self.db_connection.add(new_entity)
        self.db_connection.commit()
        self.db_connection.refresh(new_entity)
        return self.DomainModel.from_orm(new_entity)

    def get(self, skip: int = 0, limit: int = 100) -> List[T]:
        result = self.db_connection.query(self.DatabaseEntity).offset(skip).limit(limit).all()
        return result

    def get_by_id(self, request_id: Integer) -> T:
        entity = self._get_by_id(request_id)
        entity = entity.first()
        if entity is None:
            raise EntityNotFoundError
        return self.DomainModel.from_orm(entity)

    def _get_by_id(self, request_id: Integer):
        entity = self.db_connection.query(self.DatabaseEntity).filter(self.DatabaseEntity.id == request_id)
        return entity

    @staticmethod
    def _get_changed_data(old_entity: BaseModel, updated_entity: BaseModel):
        updated_data = {}
        for key, value in updated_entity.dict().items():
            if hasattr(old_entity, key) and value != getattr(old_entity, key):
                updated_data[key] = value

        return updated_data

    def update(self, request_id: Integer, model: BaseModel) -> T:
        current = self._get_by_id(request_id)
        if current.first() is None:
            raise EntityNotFoundError
        current.update(self._get_changed_data(old_entity=current.first(), updated_entity=model))
        self.db_connection.commit()

        updated = self.get_by_id(request_id)
        return self.DomainModel.from_orm(updated)

    def delete(self, request_id: Integer):
        entity = self._get_by_id(request_id).first()
        if entity is None:
            raise EntityNotFoundError
        self.db_connection.delete(entity)
        self.db_connection.commit()
