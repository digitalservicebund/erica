from fastapi import APIRouter

from erica.api.v2.endpoints import ping, est, grundsteuer, tax, fsc, management

api_router_02 = APIRouter()
api_router_02.prefix = '/v2'

api_router_02.include_router(ping.router, prefix="/ping", tags=["Ping"])
api_router_02.include_router(est.router, tags=["Steuererklärung"])
api_router_02.include_router(grundsteuer.router, prefix="/grundsteuer", tags=["Grundsteuererklärung"])
api_router_02.include_router(tax.router, tags=["Finanzverwaltung"])
api_router_02.include_router(fsc.router, prefix="/fsc", tags=["Freischaltcode"])
api_router_02.include_router(management.router, prefix="/management", tags=["Management"])
