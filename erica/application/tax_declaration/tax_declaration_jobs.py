import logging

from erica.application.JobService.job import perform_job
from erica.domain.Shared.EricaAuftrag import RequestType


async def send_est(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    service = get_job_service(RequestType.send_est)
    await perform_job(request_id=request_id,
                repository=service.repository,
                service=service,
                dto=service.payload_type,
                logger=logging.getLogger())
