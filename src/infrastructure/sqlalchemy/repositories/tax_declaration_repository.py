from abc import ABC

from opyoid import Injector
from sqlalchemy.orm import Session

from src.domain.TaxDeclaration.TaxDeclaration import TaxDeclaration
from src.infrastructure.InfrastructureModule import InfrastructureModule
from src.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository
from src.infrastructure.sqlalchemy.TaxDeclaration import TaxDeclarationEntity

injector = Injector([InfrastructureModule()])


class TaxDeclarationRepository(BaseRepository[TaxDeclaration, TaxDeclarationEntity], ABC):
    def __init__(self, db_connection: Session = injector.inject(Session)):
        super().__init__(db_connection)
        self.entity = TaxDeclarationEntity
