from abc import ABCMeta, abstractmethod
from uuid import UUID

from opyoid import Module

from erica.erica_api.service.base_service import BaseService
from erica.erica_api.dto.response_dto import JobState, ResultTransferPdfResponseDto
from erica.erica_api.service.response_state_mapper import map_status
from erica.erica_api.dto.grundsteuer_dto import GrundsteuerResponseDto
from erica.erica_shared.model.erica_request import RequestType


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
                transferticket=erica_request.result["transferticket"],
                pdf=erica_request.result["pdf"])
            return GrundsteuerResponseDto(
                process_status=map_status(erica_request.status), result=result)
        elif process_status == JobState.FAILURE:
            return GrundsteuerResponseDto(
                process_status=map_status(erica_request.status), error_code=erica_request.error_code,
                error_message=erica_request.error_message, result=erica_request.result)
        else:
            return GrundsteuerResponseDto(
                process_status=map_status(erica_request.status))


class GrundsteuerServiceModule(Module):
    def configure(self) -> None:
        self.bind(GrundsteuerServiceInterface, to_class=GrundsteuerService)
