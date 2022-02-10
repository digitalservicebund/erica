from fastapi import APIRouter

from erica.api.v2.rente import est, tax, address, unlock_code, job

api_router_02 = APIRouter()
api_router_02.prefix = '/02'

api_router_02.include_router(address.router, prefix="/address", tags=["Adresse"])
api_router_02.include_router(est.router, tags=["Steuererklärung"])
api_router_02.include_router(tax.router, tags=["Steuer"])
api_router_02.include_router(unlock_code.router, tags=["Freischaltcode"])
api_router_02.include_router(job.router, prefix="/job", tags=["Jobstatus"])

