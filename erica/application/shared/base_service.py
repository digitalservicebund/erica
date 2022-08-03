from uuid import UUID
from erica.application.erica_request.erica_request_service import EricaRequestService
from erica.application.errors.errors import RequestTypeDoesNotMatchEndpointError
from erica.domain.shared.erica_request import RequestType


class BaseService:
    erica_request_service: EricaRequestService

    def __init__(self, service: EricaRequestService) -> None:
        super().__init__()
        self.erica_request_service = service

    def get_erica_request(self, request_id: UUID, request_type: RequestType):
        erica_request = self.erica_request_service.get_request_by_request_id(request_id)
        if erica_request.type != request_type:
            raise RequestTypeDoesNotMatchEndpointError(erica_request.type, request_type)
        return erica_request
