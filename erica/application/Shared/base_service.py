from uuid import UUID
from erica.application.erica_request.erica_request_service import EricaRequestService


class BaseService:
    erica_request_service: EricaRequestService

    def __init__(self, service: EricaRequestService) -> None:
        super().__init__()
        self.erica_request_service = service

    def get_erica_request(self, request_id: UUID):
        return self.erica_request_service.get_request_by_request_id(request_id)
