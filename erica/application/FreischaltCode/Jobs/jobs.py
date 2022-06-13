import logging

from erica.application.JobService.job import perform_job
from erica.domain.Shared.EricaRequest import RequestType
from erica.infrastructure.sqlalchemy.database import session_scope

async def request_freischalt_code(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.freischalt_code_request)
        await perform_job(request_id=request_id,
                        repository=service.repository,
                        service=service,
                        payload_type=service.payload_type,
                        logger=logging.getLogger())


async def activate_freischalt_code(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.freischalt_code_activate)
        await perform_job(request_id=request_id,
                        repository=service.repository,
                        service=service,
                        payload_type=service.payload_type,
                        logger=logging.getLogger())


async def revocate_freischalt_code(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    with session_scope():
        service = get_job_service(RequestType.freischalt_code_revocate)
        await perform_job(request_id=request_id,
                        repository=service.repository,
                        service=service,
                        payload_type=service.payload_type,
                        logger=logging.getLogger())
