from fastapi import APIRouter

from erica.erica_legacy.api.v1.api_v1 import api_router_01

api_router = APIRouter()

api_router.include_router(api_router_01)
