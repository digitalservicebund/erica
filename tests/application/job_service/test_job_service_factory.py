import pytest

from erica.application.EricRequestProcessing.requests_controller import UnlockCodeActivationRequestController
from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto
from erica.application.JobService.job_service_factory import get_job_service
from erica.infrastructure.rq.BackgroundJobRq import BackgroundJobRq
from erica.infrastructure.sqlalchemy.repositories.EricaAuftragRepository import EricaAuftragRepository


class TestJobServiceFactory:

    def test_if_unknown_dto_as_input_then_raise_not_implemented_error(self):
        class NotFoundDto(BaseDto):
            pass

        with pytest.raises(NotImplementedError):
            get_job_service(NotFoundDto)

    def test_if_fsc_activate_dto_then_return_correctly_configured_dto(self):
        job_service = get_job_service(FreischaltCodeActivateDto.parse_obj(
                {'idnr': "1234",
                 'freischalt_code': "DBNE-DBD1-1YDI",
                 'elster_request_id': "007"})
            )

        assert isinstance(job_service.repository, EricaAuftragRepository)
        assert isinstance(job_service.background_worker, BackgroundJobRq)
        assert isinstance(job_service.payload_type, FreischaltCodeActivateDto)
        assert issubclass(job_service.request_controller, UnlockCodeActivationRequestController)

