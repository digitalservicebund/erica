from fastapi import APIRouter

from erica.api.v2.endpoints import ping
from erica.api.v2.endpoints.rente import unlock_code, est, tax


api_router_02 = APIRouter()
api_router_02.prefix = '/02'

api_router_02.include_router(ping.router, prefix="/ping", tags=["Ping"])
api_router_02.include_router(est.router, tags=["Steuererklärung"])
api_router_02.include_router(tax.router, tags=["Finanzverwaltung"])
api_router_02.include_router(unlock_code.router, prefix="/unlock_code", tags=["Freischaltcode"])



