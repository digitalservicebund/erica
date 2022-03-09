from opyoid import Injector
from sqlalchemy.orm import Session

from src.domain.FreischaltCode.FreischaltCode import FreischaltCode
from src.infrastructure.InfrastructureModule import InfrastructureModule
from src.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository
from src.infrastructure.sqlalchemy.FreischaltCodeActivateSchema import FreischaltCodeActivateSchema

injector = Injector([InfrastructureModule()])


class FreischaltCodeActivateRepository(BaseRepository[FreischaltCode, FreischaltCodeActivateSchema]):
    def __init__(self, db_connection: Session = injector.inject(Session)):
        super().__init__(db_connection)
        self.entity = FreischaltCodeActivateSchema
