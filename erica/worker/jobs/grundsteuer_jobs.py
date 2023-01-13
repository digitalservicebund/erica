import logging

from erica.worker.jobs.job import perform_job
from erica.worker.huey import huey
from erica.domain.model.erica_request import RequestType
from erica.domain.sqlalchemy.database import session_scope


@huey.task(expires=240)
def send_grundsteuer(request_id):
    with session_scope():
        from erica.job_service.job_service_factory import get_job_service
        service = get_job_service(RequestType.grundsteuer)
        perform_job(request_id=request_id,
                    repository=service.repository,
                    service=service,
                    payload_type=service.payload_type,
                    logger=logging.getLogger())
