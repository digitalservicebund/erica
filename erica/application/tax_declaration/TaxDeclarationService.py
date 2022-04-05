from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module
from erica.application.Shared.response_dto import JobState
from erica.application.Shared.response_state_mapper import map_status
from erica.application.erica_request.erica_request_service import EricaRequestService
from erica.application.tax_declaration.tax_declaration_dto import EstResponseDto, ResultEstResponseDto


class TaxDeclarationServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_response_send_est(self, request_id: UUID) -> EstResponseDto:
        pass


class TaxDeclarationService(TaxDeclarationServiceInterface):
    erica_request_service: EricaRequestService

    def __init__(self, service: EricaRequestService) -> None:
        super().__init__()
        self.erica_request_service = service

    def get_response_send_est(self, request_id: UUID):
        erica_request = self.erica_request_service.get_request_by_request_id(request_id)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = ResultEstResponseDto(
                transfer_ticket=erica_request.result["transfer_ticket"],
                pdf=erica_request.result["pdf"])
            return EstResponseDto(
                processStatus=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return EstResponseDto(
                processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
                errorMessage=erica_request.error_message)
        else:
            return EstResponseDto(
                processStatus=map_status(erica_request.status))


class TaxDeclarationServiceModule(Module):
    def configure(self) -> None:
        self.bind(TaxDeclarationServiceInterface, to_class=TaxDeclarationService)
