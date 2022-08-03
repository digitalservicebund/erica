from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module

from erica.erica_api.service.base_service import BaseService
from erica.erica_api.dto.response_dto import JobState, ResultTransferPdfResponseDto
from erica.erica_api.service.response_state_mapper import map_status
from erica.erica_api.dto.tax_declaration_dto import EstResponseDto
from erica.erica_shared.model.erica_request import RequestType


class TaxDeclarationServiceInterface(BaseService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_response_send_est(self, request_id: UUID) -> EstResponseDto:
        pass


class TaxDeclarationService(TaxDeclarationServiceInterface):

    def get_response_send_est(self, request_id: UUID):
        erica_request = self.get_erica_request(request_id, RequestType.send_est)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = ResultTransferPdfResponseDto(
                transferticket=erica_request.result["transferticket"],
                pdf=erica_request.result["pdf"])
            return EstResponseDto(
                process_status=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return EstResponseDto(
                process_status=map_status(erica_request.status), error_code=erica_request.error_code,
                error_message=erica_request.error_message, result=erica_request.result)
        else:
            return EstResponseDto(
                process_status=map_status(erica_request.status))


class TaxDeclarationServiceModule(Module):
    def configure(self) -> None:
        self.bind(TaxDeclarationServiceInterface, to_class=TaxDeclarationService)
