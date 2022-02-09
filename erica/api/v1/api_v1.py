from fastapi import APIRouter
from erica.api.v1.endpoints.rente import tax, est, address, unlock_code
from erica.api.v1.endpoints.grundsteuer import grundsteuer

api_router_01 = APIRouter()
api_router_01.prefix = '/01'

api_router_01.include_router(address.router, prefix="/address", tags=["Adresse"])
api_router_01.include_router(est.router, tags=["Steuererklärung"])
api_router_01.include_router(grundsteuer.router, prefix="/grundsteuer", tags=["Grundsteuer"])
api_router_01.include_router(tax.router, prefix="/tax_", tags=["Steuer"])
api_router_01.include_router(unlock_code.router, prefix="/unlock_code_", tags=["Freischaltcode"])
