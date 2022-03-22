from datetime import datetime
from logging import Logger
from typing import Type
from uuid import UUID

from erica.application.FreischaltCode.FreischaltCode import BaseDto
from erica.application.JobService.job_service import JobServiceInterface
from erica.domain.repositories import base_repository_interface
from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError


async def perform_job(entity_id: UUID, repository: base_repository_interface, service: JobServiceInterface, dto: Type[BaseDto], logger: Logger):
    """
    The basic implementation for a job that is put on the Erica queue. It will get an entity, interact with the ERiC
    library using the service and then update the entity according to the result from the service.

    It also measures the elapsed time during job execution.
    """
    try:
        entity: EricaRequest = repository.get_by_job_id(entity_id)
    except EntityNotFoundError:
        logger.warning(f"Entity not found for job_id {entity_id}", exc_info=True)
        raise

    request_payload: dto = dto.parse_obj(entity.payload)
    start_time = datetime.now()

    try:
        logger.info(f"Job started: {entity}", exc_info=True)

        try:
            response = await service.apply_to_elster(request_payload, True)
            entity.result = response
            entity.status = Status.success
            repository.update(entity.id, entity)
        except EricProcessNotSuccessful as e:
            logger.warning(
                f"Job failed: {entity}. Got Error Message: {e.generate_error_response(True).__str__()}",
                exc_info=True
            )
            raise

        logger.info(f"Job finished: {entity}", exc_info=True)
    finally:
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        logger.info(f"Job running time for {entity}: {elapsed_time}")