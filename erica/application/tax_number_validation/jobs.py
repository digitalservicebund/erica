import logging

from erica.application.JobService.job import perform_job
from erica.domain.Shared.EricaAuftrag import RequestType


async def check_tax_number(entity_id):
    from erica.application.JobService.job_service_factory import get_job_service
    service = get_job_service(RequestType.check_tax_number)
    await perform_job(entity_id=entity_id,
                repository=service.repository,
                service=service,
                dto=service.payload_type,
                logger=logging.getLogger())
