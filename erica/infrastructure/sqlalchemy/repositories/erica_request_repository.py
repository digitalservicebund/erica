from abc import ABC
from uuid import UUID
import datetime as dt

from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.repositories.erica_request_repository_interface import EricaRequestRepositoryInterface
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

    def get_by_job_request_id(self, request_id: UUID) -> EricaRequest:
        entity = self._get_by_job_request_id(request_id).first()
        if entity is None:
            raise EntityNotFoundError
        return self.DomainModel.from_orm(entity)

    def _get_by_job_request_id(self, request_id: UUID):
        entity = self.db_connection.query(self.DatabaseEntity).filter(self.DatabaseEntity.request_id == request_id)
        return entity

    def update_by_job_request_id(self, request_id: UUID, model: BaseModel) -> EricaRequest:
        current_query = self._get_by_job_request_id(request_id)
        current_entity = current_query.first()
        if current_entity is None:
            raise EntityNotFoundError

        # We only want to run update with changed data
        current_query.update(self._get_changed_data(current_query.first(), model))
        self.db_connection.commit()

        updated = self.get_by_job_request_id(request_id)
        return self.DomainModel.from_orm(updated)

    def delete_by_job_request_id(self, request_id: UUID):
        entity = self._get_by_job_request_id(request_id).first()
        if entity is None:
            raise EntityNotFoundError

        self.db_connection.delete(entity)
        self.db_connection.commit()

    def delete_success_fail_old_entities(self, ttl) -> int:
        stmt = self.DatabaseEntity.__table__.delete().where(
            or_(self.DatabaseEntity.status == Status.success, self.DatabaseEntity.status == Status.failed),
            self.DatabaseEntity.updated_at < dt.datetime.now() - dt.timedelta(minutes=ttl))
        deleted = self.db_connection.execute(stmt)
        self.db_connection.commit()
        return deleted.rowcount

    def update_status_not_finished_entities_to_failed(self, ttl) -> int:
        stmt = self.DatabaseEntity.__table__.update() \
            .where(or_(self.DatabaseEntity.status == Status.new, self.DatabaseEntity.status == Status.scheduled,
                       self.DatabaseEntity.status == Status.processing),
                   self.DatabaseEntity.updated_at < dt.datetime.now() - dt.timedelta(
                       minutes=ttl)).values(
            status=Status.failed, error_code="999", error_message="Request could not be processed within 2 minutes.")
        updated = self.db_connection.execute(stmt)
        self.db_connection.commit()
        return updated.rowcount
