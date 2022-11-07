import logging

from fastapi import FastAPI, Request
from fastapi_sqlalchemy import DBSessionMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from erica.api.exception_handling import generate_exception_handlers
from erica.api.v2.api_v2 import api_router_02
from erica.config import get_settings
from erica.domain.sqlalchemy.database import engine_args

# Import this here to make it available for the huey TaskRegistry https://huey.readthedocs.io/en/latest/imports.html#imports
from erica.worker.jobs.list_permission_jobs import get_idnr_status_list_with_huey


app = FastAPI(
    title="Erica Service",
    version="2.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
app.exception_handlers = generate_exception_handlers(app)

app.include_router(api_router_02)

app.add_middleware(DBSessionMiddleware, db_url=get_settings().database_url, engine_args=engine_args)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # TODO Remove the split once v1 is no longer in use
    #  Split after tax_number_validity to not log any tax number information contained in the URL
    if len(request.url.path.split("tax_number_validity", 1)) > 1:
        stripped_request_url_path = request.url.path.replace(request.url.path.split("tax_number_validity", 1)[1], "")
    else:
        stripped_request_url_path = request.url.path
    logging.getLogger().info(f"Erica got request at request path={stripped_request_url_path}")

    response = await call_next(request)

    return response

# Add default metrics and expose endpoint.
Instrumentator().instrument(app).expose(app)
