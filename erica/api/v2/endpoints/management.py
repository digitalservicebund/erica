from fastapi import APIRouter
from opyoid import Injector

from erica.api.ApiModule import ApiModule
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository

router = APIRouter()

injector = Injector([
    ApiModule(),
])


@router.get("/erica_auftraege")
async def get_erica_auftrag_status_list(skip: int, limit: int):
    # TODO Don't access the repository here directly. We should use a Service instead
    repo: EricaRequestRepository = injector.inject(EricaRequestRepository)
    return repo.get(skip, limit)
