from abc import ABC

import injector as injector
from sqlalchemy.orm import Session

from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.Repositories.EricaRequestRepositoryInterface import EricaRequestRepositoryInterface
from erica.infrastructure.sqlalchemy.erica_request_schema import EricaRequestSchema
from erica.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository


class EricaRequestRepository(
    BaseRepository[EricaAuftrag, EricaRequestSchema],
    EricaRequestRepositoryInterface,
    ABC
):
    def __init__(self, db_connection: Session):
        super().__init__(db_connection)
        self.DatabaseEntity = EricaRequestSchema
        self.DomainModel = EricaAuftrag
