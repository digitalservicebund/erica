from abc import ABC
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.orm import Session

from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.Repositories.EricaRequestRepositoryInterface import EricaRequestRepositoryInterface
from erica.infrastructure.sqlalchemy.erica_request_schema import EricaRequestSchema
from erica.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository, EntityNotFoundError


class EricaRequestRepository(
    BaseRepository[EricaRequest, EricaRequestSchema],
    EricaRequestRepositoryInterface,
    ABC
):
    def __init__(self, db_connection: Session):
        super().__init__(db_connection)
        self.DatabaseEntity = EricaRequestSchema
        self.DomainModel = EricaRequest

    def get_by_job_id(self, job_id: UUID) -> EricaRequest:
        entity = self._get_by_job_id(job_id).first()
        if entity is None:
            raise EntityNotFoundError
        return self.DomainModel.from_orm(entity)

    def _get_by_job_id(self, job_id: UUID):
        entity = self.db_connection.query(self.DatabaseEntity).filter(self.DatabaseEntity.job_id == job_id)
        return entity

    def update_by_job_id(self, job_id: UUID, model: BaseModel) -> EricaRequest:
        current = self._get_by_job_id(job_id)
        current.update(model.dict())
        self.db_connection.commit()

        updated = self.get_by_job_id(job_id)
        return self.DomainModel.from_orm(updated)

    def delete_by_job_id(self, job_id: UUID):
        entity = self._get_by_job_id(job_id).first()
        if entity is None:
            raise EntityNotFoundError

        self.db_connection.delete(entity)
        self.db_connection.commit()
