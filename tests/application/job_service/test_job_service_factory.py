import pytest

from erica.application.EricRequestProcessing.requests_controller import UnlockCodeActivationRequestController
from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto
from erica.application.JobService.job_service_factory import get_job_service
from erica.domain.Shared.EricaAuftrag import RequestType
from erica.infrastructure.rq.BackgroundJobRq import BackgroundJobRq
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


class TestJobServiceFactory:

    def test_if_unknown_dto_as_input_then_raise_not_implemented_error(self):
        class NotFoundDto(BaseDto):
            pass

        with pytest.raises(NotImplementedError):
            get_job_service(NotFoundDto)

    def test_if_fsc_activate_type_then_return_correctly_configured_dto(self):
        job_service = get_job_service(RequestType.freischalt_code_activate)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert isinstance(job_service.background_worker, BackgroundJobRq)
        assert issubclass(job_service.payload_type, FreischaltCodeActivateDto)
        assert issubclass(job_service.request_controller, UnlockCodeActivationRequestController)

