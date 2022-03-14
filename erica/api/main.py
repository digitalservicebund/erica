from uuid import UUID
from fastapi import FastAPI
from opyoid import Injector

from erica.api.ApiModule import ApiModule
from erica.application.EricaAuftrag.EricaAuftrag import EricaAuftragDto
from erica.application.EricaAuftrag.EricaAuftragService import EricaAuftragServiceInterface
from erica.application.FreischaltCode.FreischaltCode import FreischaltCodeBeantragenDto

from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeServiceInterface
from erica.application.TaxDeclaration.TaxDeclaration import TaxDeclarationValidateDto
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

# @app.get("/tax_declarations")
# @version(1, 0)
# async def get_tax_declarations(skip: int, limit: int,
#                                repo: TaxDeclarationRepository = Depends(TaxDeclarationRepository)):
#     return repo.get(skip, limit)
#
#
# @app.get("/tax_declarations/{id}")
# @version(1, 0)
# async def get_tax_declaration(entity_id: UUID,
#                               tax_declaration_service: TaxDeclarationService = Depends(TaxDeclarationService)):
#     return tax_declaration_service.get_status(entity_id)
#
#
# @app.post("/tax_declarations", response_model=TaxDeclarationDto)
# @version(1, 0)
# async def create_tax_declaration(
#         tax_declaration_create_dto: TaxDeclarationCreateDto,
#         tax_declaration_service: TaxDeclarationService = Depends(TaxDeclarationService)
# ):
#     result = tax_declaration_service.create(tax_declaration_create_dto)
#     return result


@app.get('/tax_validations')
@version(1, 0)
async def get_tax_validations():
    pass


@app.get('/tax_validations/{id}')
@version(1, 0)
async def get_tax_validation():
    pass


@app.post('/tax_validations', response_model=TaxDeclarationValidateDto)
@version(1, 0)
async def create_tax_validation():
    pass


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


# @app.get("/freischalt_code_activate/{id}")
# @version(1, 0)
# async def get_freischalt_code_activate(entity_id: UUID,
#                                        freischalt_code_activation_service: FreischaltCodeActivationService =
#                                        Depends(FreischaltCodeActivationService)):
#     return freischalt_code_activation_service.get_status(entity_id)
#
#
# @app.post("/freischalt_code_activate", response_model=FreischaltCodeActivateDto)
# @version(1, 0)
# async def create_freischalt_code_activate(
#         freischalt_code_create_activate_dto: FreischaltCodeCreateActivateDto,
#         freischalt_code_activation_service: FreischaltCodeActivationService = Depends(FreischaltCodeActivationService)
# ):
#     result = freischalt_code_activation_service.create(freischalt_code_create_activate_dto)
#     return result
#
#
# @app.get("/freischalt_code_revocate/{id}")
# @version(1, 0)
# async def get_freischalt_code_revocate(entity_id: UUID,
#                                        freischalt_code_service: FreischaltCodeRevocationService =
#                                        Depends(FreischaltCodeRevocationService)):
#     return freischalt_code_service.get_status(entity_id)
#
#
# @app.post("/freischalt_code_revocate", response_model=FreischaltCodeRevocateDto)
# @version(1, 0)
# async def create_freischalt_code_revocate(
#         freischalt_code_create_revocate_dto: FreischaltCodeCreateRevocateDto,
#         freischalt_code_revocation_service: FreischaltCodeRevocationService = Depends(FreischaltCodeRevocationService)
# ):
#     result = freischalt_code_revocation_service.create(freischalt_code_create_revocate_dto)
#     return result


app = VersionedFastAPI(app)
