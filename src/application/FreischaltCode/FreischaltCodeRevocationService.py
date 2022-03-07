import datetime
from uuid import UUID

from fastapi import Depends

from src.application.FreischaltCode.FreischaltCode import FreischaltCodeCreateRevocateDto
from src.domain.FreischaltCode.FreischaltCode import FreischaltCodeRevocate
from src.infrastructure.sqlalchemy.repositories.freischalt_code_revocate_repository \
    import FreischaltCodeRevocateRepository


class FreischaltCodeRevocationService:
    freischalt_code_repository: FreischaltCodeRevocateRepository

    def __init__(self, repository: FreischaltCodeRevocateRepository = Depends(FreischaltCodeRevocateRepository)) -> None:
        super().__init__()
        self.freischalt_code_repository = repository

    def create(self, freischalt_code_dto: FreischaltCodeCreateRevocateDto):
        freischalt_code = FreischaltCodeRevocate(tax_ident=freischalt_code_dto.tax_ident,
                                                 elster_request_id=freischalt_code_dto.elster_request_id,
                                                 created_at=datetime.datetime.now().__str__(),
                                                 updated_at=datetime.datetime.now().__str__(),
                                                 creator_id="api"
                                                 )
        return self.freischalt_code_repository.create(freischalt_code)

    def send_to_elster(self):
        pass

    def get_status(self, tax_ident: UUID):
        return self.freischalt_code_repository.get_by_id(tax_ident)
