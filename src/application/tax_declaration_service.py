import datetime
from uuid import UUID

from fastapi import Depends

from src.application.tax_declaration import TaxDeclarationCreateDto
from src.domain.tax_declaration import TaxDeclaration
from src.infrastructure.sqlalchemy.repositories.tax_declaration_repository import TaxDeclarationRepository


class TaxDeclarationService:
    tax_declaration_repository: TaxDeclarationRepository

    def __init__(self, repository: TaxDeclarationRepository = Depends(TaxDeclarationRepository)) -> None:
        super().__init__()
        self.tax_declaration_repository = repository

    def create(self, tax_declaration_dto: TaxDeclarationCreateDto):
        tax_declaration = TaxDeclaration(user_id=tax_declaration_dto.user_id,
                                         payload=tax_declaration_dto.payload,
                                         created_at=datetime.datetime.now().__str__(),
                                         updated_at=datetime.datetime.now().__str__(),
                                         creator_id="api"
                                         )
        return self.tax_declaration_repository.create(tax_declaration)

    def send_to_elster(self):
        pass

    def get_status(self, tax_id: UUID):
        return self.tax_declaration_repository.get_by_id(tax_id)
