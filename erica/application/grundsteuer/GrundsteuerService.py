from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module

from erica.application.Shared.base_service import BaseService
from erica.application.Shared.response_dto import JobState, ResultTransferPdfResponseDto
from erica.application.Shared.response_state_mapper import map_status
from erica.application.grundsteuer.grundsteuer_dto import GrundsteuerResponseDto
from erica.domain.Shared.EricaRequest import RequestType


class GrundsteuerServiceInterface(BaseService):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_response_grundsteuer(self, request_id: UUID) -> GrundsteuerResponseDto:
        pass


class GrundsteuerService(GrundsteuerServiceInterface):

    def get_response_grundsteuer(self, request_id: UUID):
        erica_request = self.get_erica_request(request_id, RequestType.grundsteuer)
        process_status = map_status(erica_request.status)
        if process_status == JobState.SUCCESS:
            result = ResultTransferPdfResponseDto(
                transfer_ticket=erica_request.result["transfer_ticket"],
                pdf=erica_request.result["pdf"])
            return GrundsteuerResponseDto(
                processStatus=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return GrundsteuerResponseDto(
                processStatus=map_status(erica_request.status), errorCode=erica_request.error_code,
                errorMessage=erica_request.error_message)
        else:
            return GrundsteuerResponseDto(
                processStatus=map_status(erica_request.status))


class GrundsteuerServiceModule(Module):
    def configure(self) -> None:
        self.bind(GrundsteuerServiceInterface, to_class=GrundsteuerService)
