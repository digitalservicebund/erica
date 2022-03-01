from abc import ABC
from typing import Generic, TypeVar, List
from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.domain.base_domain_model import BaseRepositoryInterface

T = TypeVar('T')


class BaseRepository(BaseRepositoryInterface[T], Generic[T], ABC):
    entity: [T]
    db_connection: Session

    def __init__(self, db_connection: Session):
        self.db_connection = db_connection

    def create(self, model: BaseModel) -> [T]:
        new_entity = self.entity(**model.dict())
        self.db_connection.add(new_entity)
        self.db_connection.commit()
        self.db_connection.refresh(new_entity)
        return new_entity

    def get(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db_connection.query(self.entity).offset(skip).limit(limit).all()

    def get_by_id(self, entity_id: UUID) -> [T]:
        return self.db_connection.query(self.entity).filter(self.entity.id == entity_id).first()

    def update(self, entity_id: UUID, model_update_dto: BaseModel) -> [T]:
        current = self.db_connection.query(self.entity).filter(self.entity.id == entity_id).first()
        current.copy(model_update_dto)
        self.db_connection.commit()
        self.db_connection.refresh(current)
        return current

    def delete(self, entity_id: UUID) -> bool:
        entity = self.db_connection.query(self.entity).filter(self.entity.id == entity_id).first()
        self.db_connection.delete(entity)
        self.db_connection.commit()
        return True
