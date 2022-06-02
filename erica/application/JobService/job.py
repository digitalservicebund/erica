from datetime import datetime
from logging import Logger
from typing import Type
from uuid import UUID
from erica.application.JobService.job_service import JobServiceInterface
from erica.domain.repositories import base_repository_interface
from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.Shared.BaseDomainModel import BasePayload
from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful, ERIC_ERRORS_WITH_RETRY
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError


async def perform_job(request_id: UUID, repository: base_repository_interface, service: JobServiceInterface,
                      payload_type: Type[BasePayload], logger: Logger):
    """
    The basic implementation for a job that is put on the Erica queue. It will get an entity, interact with the ERiC
    library using the service and then update the entity according to the result from the service.

    It also measures the elapsed time during job execution.
    """
    try:
        entity: EricaRequest = repository.get_by_job_request_id(request_id)
    except EntityNotFoundError:
        logger.warning(f"Entity not found for request_id {request_id}", exc_info=True)
        raise

    request_payload: payload_type = payload_type.parse_obj(entity.payload)
    start_time = datetime.now()

    try:
        logger.info(f"Job started: {entity}", exc_info=True)

        try:
            response = await service.apply_to_elster(request_payload, True)
            # We do not want to send the server_response or eric_response to the clients in the success case
            response.pop('server_response', None)
            response.pop('eric_response', None)
            entity.result = response
            entity.status = Status.success
            repository.update(entity.id, entity)
        except EricProcessNotSuccessful as e:
            error_response = e.generate_error_response(True)
            logger.warning(
                f"Job failed: {entity}. Got Error Message: {error_response.__str__()}",
                exc_info=True
            )
            entity.error_code = error_response.get('message')
            entity.error_message = error_response.get('message')
            validation_problems = error_response.get('validation_problems')
            entity.result = {"validation_errors": validation_problems} if validation_problems else None
            entity.status = Status.failed
            repository.update(entity.id, entity)
            if entity.error_code in ERIC_ERRORS_WITH_RETRY:
                raise

        logger.info(f"Job finished: {entity}", exc_info=True)
    finally:
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        logger.info(f"Job running time for {entity}: {elapsed_time}")