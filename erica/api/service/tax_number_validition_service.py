from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module

from erica.api.service.base_service import BaseService
from erica.api.dto.response_dto import JobState
from erica.api.service.response_state_mapper import map_status
from erica.api.dto.tax_number_validation_dto import TaxResponseDto, ResultTaxResponseDto
from erica.shared.model.erica_request import RequestType


class TaxNumberValidityServiceInterface(BaseService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_response_tax_number_validity(self, request_id: UUID) -> TaxResponseDto:
        pass


class TaxNumberValidityService(TaxNumberValidityServiceInterface):

    def get_response_tax_number_validity(self, request_id: UUID):
        erica_request = self.get_erica_request(request_id, RequestType.check_tax_number)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = ResultTaxResponseDto(
                is_valid=erica_request.result["is_valid"])
            return TaxResponseDto(
                process_status=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return TaxResponseDto(
                process_status=map_status(erica_request.status), error_code=erica_request.error_code,
                error_message=erica_request.error_message)
        else:
            return TaxResponseDto(
                process_status=map_status(erica_request.status))


class TaxDeclarationServiceModule(Module):
    def configure(self) -> None:
        self.bind(TaxNumberValidityServiceInterface, to_class=TaxNumberValidityService)
