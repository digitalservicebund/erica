from fastapi import APIRouter
from opyoid import Injector

from erica.api.ApiModule import ApiModule
from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface

router = APIRouter()

injector = Injector([
    ApiModule(),
])


@router.get("/erica_auftraege")
async def get_erica_auftrag_status_list(skip: int, limit: int):
    freischalt_code_service: EricaAuftragServiceInterface = injector.inject(EricaAuftragServiceInterface)
    return freischalt_code_service.get_all_by_skip_and_limit(skip, limit)
