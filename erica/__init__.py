import logging
import time

from fastapi import FastAPI
from prometheus_client import Gauge
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.requests import Request
from starlette.responses import JSONResponse

from erica.api.v2.api_v2 import api_router_02
from erica.erica_legacy.api.api import api_router
from erica.config import get_settings
from erica.erica_legacy.pyeric.eric import verify_using_stick
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError

app = FastAPI(
    title="Erica Service",
    version="2.0.0",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    })


class DongleStatus:
    """
    Instrumentation helper to regularly check whether we still have a connection to the dongle.
    Caches results and only checks in fixed intervals to avoid performance penalties.
    """

    check_interval_in_seconds = 60
    last_checked = 0
    dongle_up_status = 1.0

    @classmethod
    def get(cls):
        now = time.time()
        if now - cls.last_checked > cls.check_interval_in_seconds:
            cls.dongle_up_status = 1.0 if verify_using_stick() else 0.0
            cls.last_checked = now

        return cls.dongle_up_status


if get_settings().dongle_connected:
    # Add a metric from prometheus_client - these are automatically exported by the instrumentator.
    up_metric = Gauge('up', 'Is the job available', ['job'])
    up_metric.labels(job='erica').set(1.0)  # Always 1 when the erica_app is running.
    up_metric.labels(job='dongle').set_function(DongleStatus.get)

    # Add router
    app.include_router(api_router)

app.include_router(api_router_02)


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_error(request: Request, exc: EntityNotFoundError):
    request_id = request.path_params.get('request_id')
    logging.getLogger().info(f"The requested entity {request_id} is not present in the database.")

    return JSONResponse(
        {"errorCode": "entity_not_found",
         "errorMessage": "The requested entity with id {request_id} was not found."},
        status_code=404,
    )


# Add default metrics and expose endpoint.
Instrumentator().instrument(app).expose(app)
