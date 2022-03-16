from abc import ABC

import injector as injector
from sqlalchemy.orm import Session

from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.Repositories.EricaRequestRepositoryInterface import EricaRequestRepositoryInterface
from erica.infrastructure.sqlalchemy.EricaAuftragSchema import EricaAuftragSchema
from erica.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository


class EricaRequestRepository(
    BaseRepository[EricaAuftrag, EricaAuftragSchema],
    EricaRequestRepositoryInterface,
    ABC
):
    def __init__(self, db_connection: Session = injector.inject(Session)):
        super().__init__(db_connection)
        self.DatabaseEntity = EricaAuftragSchema
        self.DomainModel = EricaAuftrag
