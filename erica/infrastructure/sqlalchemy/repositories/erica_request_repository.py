from abc import ABC

from sqlalchemy.orm import Session

from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.Repositories.EricaRequestRepositoryInterface import EricaRequestRepositoryInterface
from erica.infrastructure.sqlalchemy.erica_request_schema import EricaRequestSchema
from erica.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository


class EricaRequestRepository(
    BaseRepository[EricaRequest, EricaRequestSchema],
    EricaRequestRepositoryInterface,
    ABC
):
    def __init__(self, db_connection: Session):
        super().__init__(db_connection)
        self.DatabaseEntity = EricaRequestSchema
        self.DomainModel = EricaRequest
