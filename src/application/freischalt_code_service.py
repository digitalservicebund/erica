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
        tax_declaration = FreischaltCode(user_id=freischalt_code_dto.user_id, payload=freischalt_code_dto.payload)
        return self.freischalt_code_repository.create(tax_declaration)

    def send_to_elster(self):
        pass

    def get_status(self, tax_id: UUID):
        return self.freischalt_code_repository.get_by_id(tax_id)
