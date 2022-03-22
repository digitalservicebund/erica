from typing import Generic, TypeVar, List
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy import Integer
from sqlalchemy.orm import Session

from erica.domain.repositories.base_repository_interface import BaseRepositoryInterface
from erica.domain.Shared.BaseDomainModel import BaseDomainModel
from erica.infrastructure.sqlalchemy.erica_request_schema import BaseDbSchema


class EntityNotFoundError(Exception):
    """ Raised in case an entity could not be found in the database"""
    pass


class EntityNotFoundError(Exception):
    """ Raised in case an entity could not be found in the database"""
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

    def get_by_id(self, entity_id: Integer) -> T:
        entity = self._get_by_id(entity_id).first()
        if entity is None:
            raise EntityNotFoundError
        return self.DomainModel.from_orm(entity)

    def _get_by_id(self, entity_id: Integer):
        entity = self.db_connection.query(self.DatabaseEntity).filter(self.DatabaseEntity.id == entity_id)
        return entity

    def update(self, entity_id: Integer, model: BaseModel) -> T:
        current = self._get_by_id(entity_id)
        if current.first() is None:
            raise EntityNotFoundError
        current.update(model.dict())
        self.db_connection.commit()

        updated = self.get_by_id(entity_id)
        return self.DomainModel.from_orm(updated)

    def delete(self, entity_id: Integer):
        entity = self._get_by_id(entity_id).first()
        if entity is None:
            raise EntityNotFoundError
        self.db_connection.delete(entity)
        self.db_connection.commit()
