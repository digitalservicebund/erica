import logging

from fastapi import status, APIRouter, HTTPException

from erica.erica_legacy.pyeric.eric_errors import EricProcessNotSuccessful
from erica.application.grundsteuer.grundsteuer_dto import GrundsteuerPayload
from erica.application.eric_request_processing.grundsteuer_request_controller import GrundsteuerRequestController

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
def send_grundsteuer(grundsteuer: GrundsteuerPayload, include_elster_responses: bool = False):
    """
    The Grundsteuer data is validated and then send to ELSTER using ERiC. If it is successful, this should return a 201
    HTTP response with {'transferticket': str, 'pdf': str}. The pdf is base64 encoded binary data of the pdf
    If there is any error with the validation, this should return a 400 response. If the validation failed with
    {‘code’ : int,‘message’: str,‘description’: str, ‘validation_problems’ : [{‘code’: int, ‘message’: str}]}
    or a 400 repsonse for other client errors and a 500 response for server errors with
    {‘code’ : int,‘message’: str,‘description’: str}

    :param grundsteuer: the JSON input data for the grundsteuer tax declaration
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = GrundsteuerRequestController(grundsteuer, include_elster_responses)
        result = request.process()
        if "transferticket" in result:
            result["transfer_ticket"] = result.pop("transferticket")
        return result
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not send grundsteuer", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))
