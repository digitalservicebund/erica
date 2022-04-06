import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from erica.application.errors.errors import RequestTypeDoesNotMatchEndpointError
from erica.domain.Shared.EricaRequest import RequestType
from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError

job_type_to_endpoint = {
    RequestType.freischalt_code_request: 'fsc/request/',
    RequestType.freischalt_code_activate: 'fsc/activation/',
    RequestType.freischalt_code_revocate: 'fsc/revocation/',
    RequestType.send_est: 'tax_number_validity/',
    RequestType.check_tax_number: 'ests/',
    RequestType.grundsteuer: 'grundsteuer/',
}


def generate_exception_handlers():
    async def entity_not_found_error(request: Request, exc: EntityNotFoundError):
        request_id = request.path_params.get('request_id')
        logging.getLogger().info(f"The requested entity {request_id} is not present in the database.")

        return JSONResponse(
            {"errorCode": "entity_not_found",
             "errorMessage": f"The requested entity with id {request_id} was not found."},
            status_code=404,
        )

    async def jop_type_mismatch_error(request: Request, exc: RequestTypeDoesNotMatchEndpointError) -> RedirectResponse:
        request_id = request.path_params.get('request_id')
        redirection_url = job_type_to_endpoint[exc.actual_type] + request_id
        logging.getLogger().info(
            f"The requested entity {request_id} was requested with the incorrect type {exc.requested_type}. Redirect to {redirection_url}")
        return RedirectResponse(url=redirection_url, status_code=309)

    async def internal_server_error(request: Request, exc: Exception):
        request_id = request.path_params.get('request_id')
        logging.getLogger().error(f"Request for entity {request_id} producted unexpected error: {str(exc)}")
        return JSONResponse(
            {"errorCode": "internal_server_error",
             "errorMessage": "An unexpected error occurred."},
            status_code=500,
        )

    exception_handlers = {
        EntityNotFoundError: entity_not_found_error,
        RequestTypeDoesNotMatchEndpointError: jop_type_mismatch_error,
        Exception: internal_server_error,
    }

    return exception_handlers
