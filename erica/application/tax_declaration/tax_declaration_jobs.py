import logging

from erica.application.job_service.job import perform_job
from erica.erica_worker.huey import huey
from erica.domain.Shared.EricaRequest import RequestType
from erica.erica_shared.sqlalchemy.database import session_scope


@huey.task()
def send_est(request_id):
    from erica.application.job_service.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.send_est)
        perform_job(request_id=request_id,
                    repository=service.repository,
                    service=service,
                    payload_type=service.payload_type,
                    logger=logging.getLogger())
