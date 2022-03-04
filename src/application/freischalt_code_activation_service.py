import datetime
from uuid import UUID

from fastapi import Depends

from src.application.freischalt_code import FreischaltCodeCreateActivateDto
from src.domain.freischalt_code import FreischaltCodeActivate
from src.infrastructure.sqlalchemy.repositories.freischalt_code_activate_repository import \
    FreischaltCodeActivateRepository


class FreischaltCodeActivationService:
    freischalt_code_repository: FreischaltCodeActivateRepository

    def __init__(self, repository: FreischaltCodeActivateRepository = Depends(FreischaltCodeActivateRepository)) -> None:
        super().__init__()
        self.freischalt_code_repository = repository

    def create(self, freischalt_code_dto: FreischaltCodeCreateActivateDto):
        freischalt_code = FreischaltCodeActivate(tax_ident=freischalt_code_dto.tax_ident,
                                                 elster_request_id=freischalt_code_dto.elster_request_id,
                                                 freischalt_code=freischalt_code_dto.freischalt_code,
                                                 created_at=datetime.datetime.now().__str__(),
                                                 updated_at=datetime.datetime.now().__str__(),
                                                 creator_id="api"
                                                 )
        return self.freischalt_code_repository.create(freischalt_code)

    def send_to_elster(self):
        pass

    def get_status(self, tax_ident: UUID):
        return self.freischalt_code_repository.get_by_id(tax_ident)
