import logging

from fastapi import Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from erica.erica_api.errors import RequestTypeDoesNotMatchEndpointError
from erica.erica_shared.model.erica_request import RequestType
from erica.erica_shared.sqlalchemy.repositories.base_repository import EntityNotFoundError

job_type_to_endpoint = {
    RequestType.freischalt_code_request: 'get_fsc_request_job',
    RequestType.freischalt_code_activate: 'get_fsc_activation_job',
    RequestType.freischalt_code_revocate: 'get_fsc_revocation_job',
    RequestType.send_est: 'get_send_est_job',
    RequestType.check_tax_number: 'get_valid_tax_number_job',
    RequestType.grundsteuer: 'get_grundsteuer_job',
}


def generate_exception_handlers(app):
    async def entity_not_found_error(request: Request, exc: EntityNotFoundError):
        request_id = request.path_params.get('request_id')
        logging.getLogger().info(f"The requested entity {request_id} is not present in the database.")

        return JSONResponse(
            {"errorCode": exc.__class__.__name__,
             "errorMessage": f"The requested entity with id {request_id} was not found."},
            status_code=404,
        )

    async def jop_type_mismatch_error(request: Request, exc: RequestTypeDoesNotMatchEndpointError) -> RedirectResponse:
        request_id = request.path_params.get('request_id')
        redirection_url = app.url_path_for(job_type_to_endpoint[exc.actual_type], request_id=request_id)
        logging.getLogger().info(
            f"The requested entity {request_id} was requested with the incorrect type {exc.requested_type}. Redirect to {redirection_url}")
        return JSONResponse(
            {"errorCode": exc.__class__.__name__,
             "errorMessage": f"The actual location of the request id {request_id} is {redirection_url}"},
            status_code=404,
        )

    async def internal_server_error(request: Request, exc: Exception):
        request_id = request.path_params.get('request_id')
        logging.getLogger().error(f"Request for entity {request_id} produced unexpected error: {str(exc)}")
        return JSONResponse(
            {"errorCode": "internal_server_error",
             "errorMessage": "An unexpected error occurred."},
            status_code=500,
        )

    async def request_http_error(request: Request, exc: HTTPException):
        if str(request.url).removeprefix(str(request.base_url)).startswith("01"):
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )
        else:
            raise exc

    # Re-using the default FastAPIs exception handler for RequestValidationError (needed for v1)
    # Needed because otherwise the handler "internal_server_error" would also catch these
    async def request_validation_error(request: Request, exc: RequestValidationError):
        request_id = request.path_params.get('request_id')
        logging.getLogger().error(f"Request for entity {request_id} had invalid input payload: {str(exc)}")
        if str(request.url).removeprefix(str(request.base_url)).startswith("01"):
            return await request_validation_exception_handler(request, exc)
        else:
            return JSONResponse(
                {"errorCode": exc.__class__.__name__,
                 "errorMessage": exc.errors()},
                status_code=422,
            )

    exception_handlers = {
        RequestValidationError: request_validation_error,
        HTTPException: request_http_error,
        EntityNotFoundError: entity_not_found_error,
        RequestTypeDoesNotMatchEndpointError: jop_type_mismatch_error,
        Exception: internal_server_error,
    }

    return exception_handlers
