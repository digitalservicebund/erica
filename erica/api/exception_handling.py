import logging

from fastapi import Request
from fastapi.responses import JSONResponse


from erica.infrastructure.sqlalchemy.repositories.base_repository import EntityNotFoundError


def generate_exception_handlers():

    async def entity_not_found_error(request: Request, exc: EntityNotFoundError):
        request_id = request.path_params.get('request_id')
        logging.getLogger().info(f"The requested entity {request_id} is not present in the database.")

        return JSONResponse(
            {"errorCode": "entity_not_found",
             "errorMessage": "The requested entity with id {request_id} was not found."},
            status_code=404,
        )

    exception_handlers = {
        EntityNotFoundError: entity_not_found_error,
    }

    return exception_handlers
