import logging

from fastapi import HTTPException, status, APIRouter
from erica.worker.request_processing.erica_input.v1.erica_input import UnlockCodeRequestData, UnlockCodeActivationData, \
    UnlockCodeRevocationData
from erica.worker.pyeric.eric_errors import EricProcessNotSuccessful
from erica.worker.request_processing.requests_controller import UnlockCodeRequestController, \
    UnlockCodeActivationRequestController, UnlockCodeRevocationRequestController

router = APIRouter()


@router.post('/unlock_code_requests', status_code=status.HTTP_201_CREATED)
def request_unlock_code(unlock_code_request: UnlockCodeRequestData, include_elster_responses: bool = False):
    """
    A new unlock code for the sent id_nr is requested. If everything is successful, return a 200 HTTP response
    with {'elster_request_id': str, 'idnr': str}. If there is any error  return a 400 repsonse for client
    errors and a 500 response for server errors with  {‘code’ : int, ‘message’: str,‘description’: str}

    :param unlock_code_request: the JSON input data for the request
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = UnlockCodeRequestController(unlock_code_request, include_elster_responses)
        result = request.process()
        if "transferticket" in result:
            result["transfer_ticket"] = result.pop("transferticket")
        return result
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not request unlock code", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))


@router.post('/unlock_code_activations', status_code=status.HTTP_201_CREATED)
def activate_unlock_code(unlock_code_activation: UnlockCodeActivationData, include_elster_responses: bool = False):
    """
    An unlock code is used activated for the sent id_nr. If everything is successful, return a 200 HTTP response
    with {'id_nr': str}. If there is any error  return a 400 response for client
    errors and a 500 response for server errors with  {‘code’ : int,‘message’: str,‘description’: str}.

    :param unlock_code_activation: the JSON input data for the activation
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = UnlockCodeActivationRequestController(unlock_code_activation, include_elster_responses)
        result = request.process()
        if "transferticket" in result:
            result["transfer_ticket"] = result.pop("transferticket")
        return result
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not activate unlock code", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))


@router.post('/unlock_code_revocations', status_code=status.HTTP_200_OK)
def revoke_unlock_code(unlock_code_revocation: UnlockCodeRevocationData, include_elster_responses: bool = False):
    """
    The permission at Elster is revoked. If everything is successful, return a 200 HTTP response
    with {'id_nr': str}. If there is any error return a 400 response for client
    errors and a 500 response for server errors with {‘code’ : int, ‘message’: str, ‘description’: str}.
    Especially, an error is returned if there is no activated or not activated unlock_code for the corresponding idnr.

    :param unlock_code_revocation: the JSON input data for the revocation
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    try:
        request = UnlockCodeRevocationRequestController(unlock_code_revocation, include_elster_responses)
        result = request.process()
        if "transferticket" in result:
            result["transfer_ticket"] = result.pop("transferticket")
        return result
    except EricProcessNotSuccessful as e:
        logging.getLogger().info("Could not revoke unlock code", exc_info=True)
        raise HTTPException(status_code=422, detail=e.generate_error_response(include_elster_responses))
