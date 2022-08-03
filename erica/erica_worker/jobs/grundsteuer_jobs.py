import logging

from erica.erica_worker.jobs.job import perform_job
from erica.erica_worker.huey import huey
from erica.erica_shared.model.erica_request import RequestType
from erica.erica_shared.sqlalchemy.database import session_scope


@huey.task()
def send_grundsteuer(request_id):
    with session_scope():
        from erica.erica_shared.job_service.job_service_factory import get_job_service
        service = get_job_service(RequestType.grundsteuer)
        perform_job(request_id=request_id,
                    repository=service.repository,
                    service=service,
                    payload_type=service.payload_type,
                    logger=logging.getLogger())
