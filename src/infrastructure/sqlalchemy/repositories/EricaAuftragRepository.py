from abc import ABC

import injector as injector
from sqlalchemy.orm import Session

from src.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from src.domain.Repositories.EricaAuftragRepositoryInterface import EricaAuftragRepositoryInterface
from src.infrastructure.sqlalchemy.EricaAuftragSchema import EricaAuftragSchema
from src.infrastructure.sqlalchemy.repositories.BaseRepository import BaseRepository


class EricaAuftragRepository(
    BaseRepository[EricaAuftrag, EricaAuftragSchema],
    EricaAuftragRepositoryInterface,
    ABC
):
    def __init__(self, db_connection: Session = injector.inject(Session)):
        super().__init__(db_connection)
        self.DatabaseEntity = EricaAuftragSchema
        self.DomainModel = EricaAuftrag
