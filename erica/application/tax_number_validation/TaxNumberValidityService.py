from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module

from erica.application.Shared.base_service import BaseService
from erica.application.Shared.response_dto import JobState
from erica.application.Shared.response_state_mapper import map_status
from erica.application.tax_number_validation.check_tax_number_dto import TaxResponseDto, ResultTaxResponseDto


class TaxNumberValidityServiceInterface(BaseService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_response_tax_number_validity(self, request_id: UUID) -> TaxResponseDto:
        pass


class TaxNumberValidityService(TaxNumberValidityServiceInterface):

    def get_response_tax_number_validity(self, request_id: UUID):
        erica_request = self.get_erica_request(request_id)
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
