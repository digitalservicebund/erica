from fastapi import APIRouter
from opyoid import Injector

from erica.api.ApiModule import ApiModule
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository

router = APIRouter()

injector = Injector([
    ApiModule(),
])


@router.get("/erica_auftraege")
async def get_erica_auftrag_status_list(skip: int, limit: int):
    repo: EricaAuftragRepository = injector.inject(EricaAuftragRepository)
    return repo.get(skip, limit)
