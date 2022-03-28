from fastapi import FastAPI
from erica.api.v2.api_v2 import api_router_02
from erica.infrastructure.sqlalchemy.database import run_migrations


run_migrations()
app = FastAPI(
    title="Erica Service",
    version="2.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    })

# Add router
app.include_router(api_router_02)
