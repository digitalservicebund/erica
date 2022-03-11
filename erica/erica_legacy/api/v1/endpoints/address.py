from fastapi import status, APIRouter
from erica.erica_legacy.request_processing.erica_input.v1.erica_input import GetAddressData

router = APIRouter()


@router.post('/', status_code=status.HTTP_200_OK)
def get_address(get_address: GetAddressData, include_elster_responses: bool = False):
    """
    The address data of the given idnr is requested at Elster and returned. Be aware, that you need a permission
    (aka an activated unlock_code) to query a person's data.

    :param get_address: the JSON input data for the request
    :param include_elster_responses: query parameter which indicates whether the ERiC/Server response are returned
    """
    # For now, we do not allow data requests as we cannot guarantee that Elster already has the relevant data gathered
    raise NotImplementedError()
