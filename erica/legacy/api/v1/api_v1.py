from fastapi import APIRouter

from erica.legacy.api.v1.endpoints import ping, unlock_code, grundsteuer, address, tax, est

api_router_01 = APIRouter()
api_router_01.prefix = '/01'

api_router_01.include_router(ping.router, prefix="/ping", tags=["Ping"])
api_router_01.include_router(address.router, prefix="/address", tags=["Adresse"])
api_router_01.include_router(est.router, tags=["Steuererklärung"])
api_router_01.include_router(grundsteuer.router, prefix="/grundsteuer", tags=["Grundsteuer"])
api_router_01.include_router(tax.router, tags=["Finanzverwaltung"])
api_router_01.include_router(unlock_code.router, tags=["Freischaltcode"])
