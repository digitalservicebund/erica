import logging

from erica.application.JobService.job import perform_job
from erica.domain.Shared.EricaRequest import RequestType


async def send_grundsteuer(request_id):
    from erica.application.JobService.job_service_factory import get_job_service
    service = get_job_service(RequestType.grundsteuer)
    await perform_job(request_id=request_id,
                      repository=service.repository,
                      service=service,
                      payload_type=service.payload_type,
                      logger=logging.getLogger())
