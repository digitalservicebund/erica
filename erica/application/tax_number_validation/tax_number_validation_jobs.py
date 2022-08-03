import logging

from erica.application.job_service.job import perform_job
from erica.erica_worker.huey import huey
from erica.domain.shared.erica_request import RequestType
from erica.erica_shared.sqlalchemy.database import session_scope


@huey.task()
def check_tax_number(request_id):
    from erica.application.job_service.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.check_tax_number)
        perform_job(request_id=request_id,
                    repository=service.repository,
                    service=service,
                    payload_type=service.payload_type,
                    logger=logging.getLogger())
