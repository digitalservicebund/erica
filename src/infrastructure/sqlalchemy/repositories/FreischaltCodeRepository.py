from abc import ABC

from opyoid import Injector
from sqlalchemy.orm import Session

from src.domain.FreischaltCode.FreischaltCode import FreischaltCode
from src.domain.Repositories.FreischaltCodeRepositoryInterface import FreischaltCodeRepositoryInterface
from src.infrastructure.InfrastructureModule import InfrastructureModule
from src.infrastructure.sqlalchemy.database import DbSession
from src.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository
from src.infrastructure.sqlalchemy.FreischaltCodeSchema import FreischaltCodeSchema

injector = Injector([InfrastructureModule()])


class FreischaltCodeRepository(
    BaseRepository[FreischaltCode, FreischaltCodeSchema],
    FreischaltCodeRepositoryInterface,
    ABC
):
    def __init__(self, db_connection: Session = injector.inject(DbSession)):
        super().__init__(db_connection)
        self.DatabaseEntity = FreischaltCodeSchema
        self.DomainModel = FreischaltCode
