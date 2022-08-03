from fastapi import APIRouter
from opyoid import Injector

from erica.api.api_module import ApiModule
from erica.application.erica_request.erica_request_service import EricaRequestServiceInterface

router = APIRouter()

injector = Injector([
    ApiModule(),
])


@router.get("/erica_requests")
async def get_erica_request_status_list(skip: int, limit: int):
    erica_request_service: EricaRequestServiceInterface = injector.inject(EricaRequestServiceInterface)
    return erica_request_service.get_all_by_skip_and_limit(skip, limit)
