import logging

from erica.application.JobService.job import perform_job, huey
from erica.domain.Shared.EricaRequest import RequestType
from erica.infrastructure.sqlalchemy.database import session_scope


@huey.task()
def request_freischalt_code(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.freischalt_code_request)
        perform_job(request_id=request_id,
                        repository=service.repository,
                        service=service,
                        payload_type=service.payload_type,
                        logger=logging.getLogger())


@huey.task()
def activate_freischalt_code(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.freischalt_code_activate)
        perform_job(request_id=request_id,
                        repository=service.repository,
                        service=service,
                        payload_type=service.payload_type,
                        logger=logging.getLogger())


@huey.task()
def revocate_freischalt_code(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.freischalt_code_revocate)
        perform_job(request_id=request_id,
                        repository=service.repository,
                        service=service,
                        payload_type=service.payload_type,
                        logger=logging.getLogger())
