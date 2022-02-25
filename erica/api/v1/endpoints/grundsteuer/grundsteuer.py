import logging

from fastapi import status, APIRouter, HTTPException

from erica.pyeric.eric_errors import EricProcessNotSuccessful
from erica.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData
from erica.request_processing.grundsteuer_request_controller import GrundsteuerRequestController

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def send_grundsteuer(grundsteuer: GrundsteuerData, include_elster_responses: bool = False):
    """
    The Grundsteuer data is validated and then send to ELSTER using ERiC. If it is successful, this should return a 201
    HTTP response with {'transfer_ticket': str, 'pdf': str}. The pdf is base64 encoded binary data of the pdf
    If there is any error with the validation, this should return a 400 response. If the validation failed with
    {‘code’ : int,‘message’: str,‘description’: str, ‘validation_problems’ : [{‘code’: int, ‘message’: str}]}
    or a 400 repsonse for other client errors and a 500 response for server errors with
    {‘code’ : int,‘message’: str,‘description’: str}

    :param grundsteuer: the JSON input data for the land tax declaration
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = GrundsteuerRequestController(grundsteuer, include_elster_responses)
        return request.process()
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not send grundsteuer", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))
