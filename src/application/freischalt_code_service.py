import datetime
from uuid import UUID

from fastapi import Depends

from src.application.freischalt_code import FreischaltCodeCreateDto
from src.domain.freischalt_code import FreischaltCode
from src.infrastructure.sqlalchemy.repositories.freischalt_code_repository import FreischaltCodeRepository


class FreischaltCodeService:
    freischalt_code_repository: FreischaltCodeRepository

    def __init__(self, repository: FreischaltCodeRepository = Depends(FreischaltCodeRepository)) -> None:
        super().__init__()
        self.freischalt_code_repository = repository

    def create(self, freischalt_code_dto: FreischaltCodeCreateDto):
        freischalt_code = FreischaltCode(tax_ident=freischalt_code_dto.tax_ident,
                                         date_of_birth=freischalt_code_dto.date_of_birth,
                                         created_at=datetime.datetime.now().__str__(),
                                         updated_at=datetime.datetime.now().__str__(),
                                         creator_id="api"
                                         )
        return self.freischalt_code_repository.create(freischalt_code)

    def send_to_elster(self):
        pass

    def get_status(self, tax_ident: UUID):
        return self.freischalt_code_repository.get_by_id(tax_ident)
