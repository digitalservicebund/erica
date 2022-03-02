from abc import ABC

from fastapi import Depends
from sqlalchemy.orm import Session

from src.infrastructure.sqlalchemy.database import get_db
from src.infrastructure.sqlalchemy.repositories.base_repository import BaseRepository
from src.infrastructure.sqlalchemy.tax_declaration import TaxDeclarationEntity


class TaxDeclarationRepository(BaseRepository[TaxDeclarationEntity], ABC):
    def __init__(self, db_connection: Session = Depends(get_db)):
        super().__init__(db_connection)
        self.entity = TaxDeclarationEntity