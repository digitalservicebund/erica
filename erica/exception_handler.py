import logging

from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.repositories import base_repository_interface

logger = logging.getLogger(__name__)


def retry_exception_handler(job, exc_type, exception, traceback):
    logger.info("Exception handling started")
    logger.info(f"Retries left: {job.retries_left}")
    if isinstance(exception, RetryException):
        if not job.retries_left:
            logger.info("Retries exhausted")
            try:
                entity: EricaRequest = exception.repository.get_by_job_request_id(job.args[0])
                error_response = exception.original_exception.generate_error_response(True)
                logger.info(f"Request id : {job.args[0]}")
                logger.info(error_response.get('message'))
                entity.error_code = error_response.get('message')
                entity.error_message = error_response.get('message')
                entity.status = Status.failed
                exception.repository.update(entity.id, entity)
                logger.info("Done handling")
            except Exception as e:
                logger.info(e)
            return False
    return True


class RetryException(Exception):

    def __init__(self, repository: base_repository_interface, original_exception):
        self.original_exception = original_exception
        self.repository = repository
