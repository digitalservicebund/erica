from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module
from erica.application.Shared.response_dto import JobState
from erica.application.Shared.response_state_mapper import map_status
from erica.application.erica_request.erica_request_service import EricaRequestService
from erica.application.tax_number_validation.check_tax_number_dto import TaxResponseDto, ResultTaxResponseDto


class TaxNumberValidityServiceInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_response_tax_number_validity(self, request_id: UUID) -> TaxResponseDto:
        pass


class TaxNumberValidityService(TaxNumberValidityServiceInterface):
    erica_request_service: EricaRequestService

    def __init__(self, service: EricaRequestService) -> None:
        super().__init__()
        self.erica_request_service = service

    def get_response_tax_number_validity(self, request_id: UUID):
        erica_request = self.erica_request_service.get_request_by_request_id(request_id)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = ResultTaxResponseDto(
                is_valid=erica_request.result["is_valid"])
            return TaxResponseDto(
                processStatus=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return TaxResponseDto(
                processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
                errorMessage=erica_request.error_message)
        else:
            return TaxResponseDto(
                processStatus=map_status(erica_request.status))


class TaxDeclarationServiceModule(Module):
    def configure(self) -> None:
        self.bind(TaxNumberValidityServiceInterface, to_class=TaxNumberValidityService)
