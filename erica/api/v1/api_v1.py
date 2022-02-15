from fastapi import APIRouter

from erica.api.v1.endpoints import ping
from erica.api.v1.endpoints.rente import tax, est, address, unlock_code
from erica.api.v1.endpoints.grundsteuer import grundsteuer

api_router_01 = APIRouter()
#api_router_01.prefix = '/01'

api_router_01.include_router(ping.router, prefix="/ping", tags=["Ping"])
api_router_01.include_router(address.router, prefix="/address", tags=["Adresse"])
api_router_01.include_router(est.router, tags=["Steuererklärung"])
api_router_01.include_router(grundsteuer.router, prefix="/grundsteuer", tags=["Grundsteuer"])
api_router_01.include_router(tax.router, tags=["Finanzverwaltung"])
api_router_01.include_router(unlock_code.router, tags=["Freischaltcode"])
