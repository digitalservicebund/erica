from datetime import datetime
from logging import Logger
from typing import Type
from uuid import UUID

from pydantic import ValidationError

from erica.job_service.job_service import JobServiceInterface
from erica.domain.repositories import base_repository_interface
from erica.domain.model.erica_request import EricaRequest, Status
from erica.domain.model.base_domain_model import BasePayload
from erica.worker.pyeric.eric_errors import EricProcessNotSuccessful, get_error_codes_from_server_err_msg, \
    EricTransferError
from erica.domain.sqlalchemy.repositories.base_repository import EntityNotFoundError


def perform_job(request_id: UUID, repository: base_repository_interface, service: JobServiceInterface,
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

    try:
        request_payload: payload_type = payload_type.parse_obj(entity.payload)
    except ValidationError as e:
        entity.error_code = "ParsingError"
        entity.error_message = "Failed to parse payload"
        entity.status = Status.failed
        repository.update(entity.id, entity)
        raise

    try:
        start_time = datetime.now()
        logger.info(f"Job started: {entity}")

        try:
            response = service.apply_to_elster(request_payload, True)
            # We do not want to send the server_response or eric_response to the clients in the success case
            response.pop('server_response', None)
            response.pop('eric_response', None)
            entity.result = response
            entity.status = Status.success
            repository.update(entity.id, entity)
        except EricProcessNotSuccessful as e:
            error_response = e.generate_error_response(True)
            transfer_errors_xml = error_response.get('server_err_msg').get('NDH_ERR_XML') if error_response.get('server_err_msg') else None

            # We only want to log the transfer codes for general EricTransferErrors
            if transfer_errors_xml and e.__class__ is EricTransferError:
                logger.warning(
                    f"Job failed: {entity}. Got error: {error_response.get('code')}. "
                    f"TransferErrors: {get_error_codes_from_server_err_msg(transfer_errors_xml)}",
                    exc_info=True
                )
            else:
                logger.warning(
                    f"Job failed: {entity}. Got error: {error_response.get('code')}.",
                    exc_info=True
                )
            entity.error_code = error_response.get('message')
            entity.error_message = error_response.get('message')
            validation_problems = error_response.get('validation_problems')
            entity.result = {"validation_errors": validation_problems} if validation_problems else None
            entity.status = Status.failed
            repository.update(entity.id, entity)

        # TODO: NF 2022-07-06: this should be logged at info level, but huey doesn't yet log properly.
        # setting the level to warning is the quickest way to get this into our production logs.
        logger.warning(f"Job finished: {entity}")
    except Exception as e:
        # Intentional bare except because this should be a catch-all
        entity.error_code = "UnkownException"
        entity.error_message = "An unknown error occurred"
        entity.status = Status.failed
        repository.update(entity.id, entity)
        raise
    finally:
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        logger.info(f"Job running time for {entity}: {elapsed_time}")
