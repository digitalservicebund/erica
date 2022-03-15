from uuid import UUID
from fastapi import FastAPI
from opyoid import Injector

from erica.api.ApiModule import ApiModule
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface
from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeBeantragenDto

from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface
from erica.infrastructure.sqlalchemy.database import run_migrations
from fastapi_versioning import VersionedFastAPI, version

from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository

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
    repo: EricaAuftragRepository = injector.inject(EricaAuftragRepository)
    return repo.get(skip, limit)


@app.get("/erica_auftraege/{id}")
@version(1, 0)
async def get_erica_auftrag_status(auftrag_id: UUID):
    freischalt_code_service: EricaAuftragServiceInterface = injector.inject(EricaAuftragServiceInterface)
    return freischalt_code_service.get_status(auftrag_id)


@app.post("/freischalt_code_beantragen", response_model=EricaAuftragDto)
@version(1, 0)
async def create_freischalt_code(freischalt_code_beantragen_dto: FreischaltCodeBeantragenDto):
    freischalt_code_service: FreischaltCodeServiceInterface = injector.inject(FreischaltCodeServiceInterface)
    result = await freischalt_code_service.freischalt_code_bei_elster_beantragen_queued(freischalt_code_beantragen_dto)
    return result


app = VersionedFastAPI(app)
