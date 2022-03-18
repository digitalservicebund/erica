import logging

from erica.application.JobService.job import perform_job
from erica.domain.Shared.EricaAuftrag import AuftragType


async def request_freischalt_code(entity_id):
    from erica.application.JobService.job_service_factory import get_job_service
    service = get_job_service(AuftragType.freischalt_code_beantragen)
    await perform_job(entity_id=entity_id,
                repository=service.repository,
                service=service,
                dto=service.payload_type,
                logger=logging.getLogger())


async def activate_freischalt_code(entity_id):
    from erica.application.JobService.job_service_factory import get_job_service
    service = get_job_service(AuftragType.freischalt_code_activate)
    await perform_job(entity_id=entity_id,
                repository=service.repository,
                service=service,
                dto=service.payload_type,
                logger=logging.getLogger())


async def revocate_freischalt_code(entity_id):
    from erica.application.JobService.job_service_factory import get_job_service
    service = get_job_service(AuftragType.freischalt_code_revocate)
    await perform_job(entity_id=entity_id,
                repository=service.repository,
                service=service,
                dto=service.payload_type,
                logger=logging.getLogger())
