import logging

from erica.application.JobService.job import perform_job
from erica.infrastructure.huey import huey
from erica.domain.Shared.EricaRequest import RequestType
from erica.infrastructure.sqlalchemy.database import session_scope


@huey.task()
def send_grundsteuer(request_id):
    with session_scope():
        from erica.application.JobService.job_service_factory import get_job_service
        service = get_job_service(RequestType.grundsteuer)
        perform_job(request_id=request_id,
                    repository=service.repository,
                    service=service,
                    payload_type=service.payload_type,
                    logger=logging.getLogger(),
                    job_type=RequestType.grundsteuer)
