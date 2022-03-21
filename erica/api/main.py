from uuid import UUID

from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version
from opyoid import Injector

from erica.api.ApiModule import ApiModule
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.EricaAuftrag.EricaAuftragService import \
    EricaAuftragServiceInterface
from erica.application.FreischaltCode.FreischaltCode import (FreischaltCodeActivateDto, FreischaltCodeRequestDto)
from erica.application.JobService.job_service_factory import get_job_service
from erica.domain.Shared.EricaAuftrag import RequestType
from erica.infrastructure.sqlalchemy.database import run_migrations
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import \
    EricaAuftragRepository
    

run_migrations()
app = FastAPI(
    title="Erica Service",
    version="1.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    })

injector = Injector([
    ApiModule(),
])


@app.get("/erica_auftraege")
@version(1, 0)
async def get_erica_auftrag_status_list(skip: int, limit: int):
    # TODO Don't access the repository here directly. We should use a Service instead
    repo: EricaAuftragRepository = injector.inject(EricaAuftragRepository)
    return repo.get(skip, limit)


@app.get("/erica_auftraege/{id}")
@version(1, 0)
async def get_erica_auftrag_status(auftrag_id: UUID):
    freischalt_code_service: EricaAuftragServiceInterface = injector.inject(EricaAuftragServiceInterface)
    return freischalt_code_service.get_status(auftrag_id)


@app.post("/freischalt_code/request", response_model=EricaAuftragDto)
@version(1, 0)
async def request_freischalt_code(freischalt_code_request_dto: FreischaltCodeRequestDto):
    return get_job_service(RequestType.freischalt_code_request).add_to_queue(freischalt_code_request_dto, RequestType.freischalt_code_request)


@app.post("/freischalt_code/activate", response_model=EricaAuftragDto)
@version(1, 0)
async def activate_freischalt_code(freischalt_code_activate_dto: FreischaltCodeActivateDto):
    return get_job_service(RequestType.freischalt_code_activate).add_to_queue(freischalt_code_activate_dto, RequestType.freischalt_code_activate)

app = VersionedFastAPI(app)
