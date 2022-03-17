from abc import ABC

import injector as injector
from sqlalchemy.orm import Session

from erica.domain.EricaAuftrag.EricaAuftrag import EricaAuftrag
from erica.domain.Repositories.EricaAuftragRepositoryInterface import EricaAuftragRepositoryInterface
from erica.infrastructure.sqlalchemy.EricaAuftragSchema import EricaAuftragSchema
from erica.infrastructure.sqlalchemy.repositories.BaseRepository import BaseRepository


class EricaAuftragRepository(
    BaseRepository[EricaAuftrag, EricaAuftragSchema],
    EricaAuftragRepositoryInterface,
    ABC
):
    def __init__(self, db_connection: Session = injector.inject(Session)):
        super().__init__(db_connection)
        self.DatabaseEntity = EricaAuftragSchema
        self.DomainModel = EricaAuftrag
