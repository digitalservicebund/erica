from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module

from erica.application.FreischaltCode.FreischaltCode import FreischaltcodeRequestAndActivationResponseDto, \
    ResultFreischaltcodeRequestAndActivationDto, FreischaltcodeRevocationResponseDto, TransferTicketAndIdnrResponseDto
from erica.application.Shared.base_service import BaseService
from erica.application.Shared.response_dto import JobState
from erica.application.Shared.response_state_mapper import map_status
from erica.domain.Shared.EricaRequest import RequestType


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
                transferticket=erica_request.result["transfer_ticket"],
                idnr=erica_request.payload.get("tax_id_number"))
            return FreischaltcodeRequestAndActivationResponseDto(
                processStatus=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return FreischaltcodeRequestAndActivationResponseDto(
                processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
                errorMessage=erica_request.error_message)
        else:
            return FreischaltcodeRequestAndActivationResponseDto(
                processStatus=map_status(erica_request.status))

    def get_response_freischaltcode_revocation(self, request_id: UUID):
        erica_request = self.get_erica_request(request_id, RequestType.freischalt_code_revocate)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = TransferTicketAndIdnrResponseDto(
                transferticket=erica_request.result["transfer_ticket"],
                idnr=erica_request.payload.get("tax_id_number"))
            return FreischaltcodeRevocationResponseDto(
                processStatus=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return FreischaltcodeRevocationResponseDto(
                processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
                errorMessage=erica_request.error_message)
        else:
            return FreischaltcodeRevocationResponseDto(
                processStatus=map_status(erica_request.status))


class FreischaltCodeServiceModule(Module):
    def configure(self) -> None:
        self.bind(FreischaltCodeServiceInterface, to_class=FreischaltCodeService)
