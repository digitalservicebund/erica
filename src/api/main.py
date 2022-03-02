from uuid import UUID
from fastapi import FastAPI, Depends

from src.application.freischalt_code import FreischaltCodeDto, FreischaltCodeCreateDto
from src.application.freischalt_code_service import FreischaltCodeService
from src.application.tax_declaration_service import TaxDeclarationService
from src.application.tax_declaration import TaxDeclarationDto, TaxDeclarationCreateDto, TaxDeclarationValidateDto
from src.infrastructure.sqlalchemy.database import run_migrations
from src.infrastructure.sqlalchemy.repositories.freischalt_code_repository import FreischaltCodeRepository
from src.infrastructure.sqlalchemy.repositories.tax_declaration_repository import TaxDeclarationRepository
from fastapi_versioning import VersionedFastAPI, version

run_migrations()
app = FastAPI(
    title="Erica Service",
    version="1.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    })


@app.get("/tax_declarations")
@version(1, 0)
async def get_tax_declarations(skip: int, limit: int,
                               repo: TaxDeclarationRepository = Depends(TaxDeclarationRepository)):
    return repo.get(skip, limit)


@app.get("/tax_declarations/{id}")
@version(1, 0)
async def get_tax_declaration(entity_id: UUID,
                              tax_declaration_service: TaxDeclarationService = Depends(TaxDeclarationService)):
    return tax_declaration_service.get_status(entity_id)


@app.post("/tax_declarations", response_model=TaxDeclarationDto)
@version(1, 0)
async def create_tax_declaration(
        tax_declaration_create_dto: TaxDeclarationCreateDto,
        tax_declaration_service: TaxDeclarationService = Depends(TaxDeclarationService)
):
    result = tax_declaration_service.create(tax_declaration_create_dto)
    return result


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


@app.get("/freischalt_codes")
@version(1, 0)
async def get_freischalt_codes(skip: int, limit: int,
                               repo: FreischaltCodeRepository = Depends(FreischaltCodeRepository)):
    return repo.get(skip, limit)


@app.get("/freischalt_codes/{id}")
@version(1, 0)
async def get_freischalt_code(entity_id: UUID,
                              freischalt_code_service: FreischaltCodeService = Depends(FreischaltCodeService)):
    return freischalt_code_service.get_status(entity_id)


@app.post("/freischalt_codes", response_model=FreischaltCodeDto)
@version(1, 0)
async def create_freischalt_code(
        freischalt_code_create_dto: FreischaltCodeCreateDto,
        freischalt_code_service: FreischaltCodeService = Depends(FreischaltCodeService)
):
    result = freischalt_code_service.create(freischalt_code_create_dto)
    return result


app = VersionedFastAPI(app)
