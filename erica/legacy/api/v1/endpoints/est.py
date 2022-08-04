import logging

from fastapi import HTTPException, status, APIRouter
from erica.worker.request_processing.erica_input.v1.erica_input import EstData
from erica.worker.pyeric.eric_errors import EricProcessNotSuccessful
from erica.worker.request_processing.requests_controller import EstValidationRequestController, EstRequestController

router = APIRouter()


@router.get('/est_validations')
def validate_est(est: EstData, include_elster_responses: bool = False):
    """
    Data for a Est is validated using ERiC. If the validation is successful then this should return
    a 200 HTTP response with {'success': bool, 'est': est}. Otherwise this should return a 400 response if the
    validation failed with {‘code’ : int,‘message’: str,‘description’: str,‘‘validation_problems’ : [{‘code’: int,
    ‘message’: str}]}  or a 400 response for other client errors and a 500 response for server errors with {‘code’ :
    int, ‘message’: str, ‘description’: str}

    :param est: the JSON input data for the ESt
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = EstValidationRequestController(est, include_elster_responses)
        result = request.process()
        if "transferticket" in result:
            result["transfer_ticket"] = result.pop("transferticket")
        return result
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not validate est", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))


@router.post('/ests', status_code=status.HTTP_201_CREATED)
def send_est(est: EstData, include_elster_responses: bool = False):
    """
    An Est is validated and then send to ELSTER using ERiC. If it is successful, this should return a 200 HTTP
    response with {'transfer_ticket': str, 'pdf': str}. The pdf is base64 encoded binary data of the pdf
    If there is any error with the validation, this should return a 400 response. If the validation failed with
    {‘code’ : int,‘message’: str,‘description’: str, ‘validation_problems’ : [{‘code’: int, ‘message’: str}]}
    or a 400 repsonse for other client errors and a 500 response for server errors with
    {‘code’ : int,‘message’: str,‘description’: str}

    :param est: the JSON input data for the ESt
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = EstRequestController(est, include_elster_responses)
        result = request.process()
        if "transferticket" in result:
            result["transfer_ticket"] = result.pop("transferticket")
        return result
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not send est", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))
