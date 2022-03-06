from abc import ABC

from opyoid import Injector
from sqlalchemy.orm import Session

from src.domain.FreischaltCode.freischalt_code import FreischaltCode
from src.infrastructure.InfrastructureModule import InfrastructureModule
from src.infrastructure.sqlalchemy.database import DbSession
from src.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository
from src.infrastructure.sqlalchemy.FreischaltCodeRevocateSchema import FreischaltCodeRevocateSchema

injector = Injector([InfrastructureModule()])


class FreischaltCodeRevocateRepository(BaseRepository[FreischaltCode, FreischaltCodeRevocateSchema], ABC):
    def __init__(self, db_connection: Session = injector.inject(DbSession)):
        super().__init__(db_connection)
        self.entity = FreischaltCodeRevocateSchema
