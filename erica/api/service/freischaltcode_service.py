from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module

from erica.api.dto.freischaltcode import FreischaltcodeRequestAndActivationResponseDto, \
    ResultFreischaltcodeRequestAndActivationDto, FreischaltcodeRevocationResponseDto, TransferticketAndIdnrResponseDto
from erica.api.service.base_service import BaseService
from erica.api.dto.response_dto import JobState
from erica.api.service.response_state_mapper import map_status
from erica.domain.model.erica_request import RequestType


class FreischaltCodeServiceInterface(BaseService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_response_freischaltcode_request(self,
                                            request_id: UUID) -> FreischaltcodeRequestAndActivationResponseDto:
        pass

    @abstractmethod
    def get_response_freischaltcode_activation(self,
                                               request_id: UUID) -> FreischaltcodeRequestAndActivationResponseDto:
        pass

    @abstractmethod
    def get_response_freischaltcode_revocation(self, request_id: UUID) -> FreischaltcodeRevocationResponseDto:
        pass


class FreischaltCodeService(FreischaltCodeServiceInterface):

    def get_response_freischaltcode_request(self, request_id: UUID):
        return self._get_base_response_freischaltcode(request_id, RequestType.freischalt_code_request)

    def get_response_freischaltcode_activation(self, request_id: UUID):
        return self._get_base_response_freischaltcode(request_id, RequestType.freischalt_code_activate)

    def _get_base_response_freischaltcode(self, request_id: UUID, request_type: RequestType):
        erica_request = self.get_erica_request(request_id, request_type)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = ResultFreischaltcodeRequestAndActivationDto(
                elster_request_id=erica_request.result["elster_request_id"],
                transferticket=erica_request.result["transferticket"],
                tax_id_number=erica_request.payload.get("tax_id_number"))
            return FreischaltcodeRequestAndActivationResponseDto(
                process_status=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return FreischaltcodeRequestAndActivationResponseDto(
                process_status=map_status(erica_request.status), error_code=erica_request.error_code,
                error_message=erica_request.error_message)
        else:
            return FreischaltcodeRequestAndActivationResponseDto(
                process_status=map_status(erica_request.status))

    def get_response_freischaltcode_revocation(self, request_id: UUID):
        erica_request = self.get_erica_request(request_id, RequestType.freischalt_code_revocate)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = TransferticketAndIdnrResponseDto(
                transferticket=erica_request.result["transferticket"],
                tax_id_number=erica_request.payload.get("tax_id_number"))
            return FreischaltcodeRevocationResponseDto(
                process_status=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return FreischaltcodeRevocationResponseDto(
                process_status=map_status(erica_request.status), error_code=erica_request.error_code,
                error_message=erica_request.error_message)
        else:
            return FreischaltcodeRevocationResponseDto(
                process_status=map_status(erica_request.status))


class FreischaltCodeServiceModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
