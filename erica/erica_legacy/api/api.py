from fastapi import APIRouter

from erica.erica_legacy.api.v1.api_v1 import api_router_01
from erica.erica_legacy.api.v2.api_v2 import api_router_02

api_router = APIRouter()

api_router.include_router(api_router_01)
api_router.include_router(api_router_02)
