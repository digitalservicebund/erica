import logging

from fastapi import status, APIRouter
from starlette.responses import JSONResponse

from erica.pyeric.utils import generate_dummy_error_response

router = APIRouter()


@router.get('/{request_id}', status_code=status.HTTP_200_OK)
def get_job_status(request_id: str):
    """
    Route for retrieving job status from the queue.
    :param request_id: the id of the job.
    """
    try:
        raise NotImplementedError()
    except NotImplementedError:
        logging.getLogger().info("Could not retrieve status of job " + request_id, exc_info=True)
        return JSONResponse(status_code=500, content=generate_dummy_error_response())

