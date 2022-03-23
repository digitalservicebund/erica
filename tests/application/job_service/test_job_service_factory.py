import pytest

from erica.application.FreischaltCode.FreischaltCode import BaseDto, FreischaltCodeActivateDto, \
    FreischaltCodeRequestDto, FreischaltCodeRevocateDto
from erica.application.JobService.job_service_factory import get_job_service
from erica.application.tax_declaration.tax_declaration_dto import TaxDeclarationDto
from erica.application.tax_number_validation.check_tax_number_dto import CheckTaxNumberDto
from erica.domain.Shared.EricaAuftrag import RequestType
from erica.erica_legacy.request_processing.requests_controller import UnlockCodeRevocationRequestController, \
    UnlockCodeRequestController, CheckTaxNumberRequestController, UnlockCodeActivationRequestController, \
    EstRequestController
from erica.infrastructure.rq.BackgroundJobRq import BackgroundJobRq
from erica.infrastructure.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository


class TestJobServiceFactory:

    def test_if_unknown_dto_as_input_then_raise_not_implemented_error(self):
        class NotFoundDto(BaseDto):
            pass

        with pytest.raises(NotImplementedError):
            get_job_service(NotFoundDto)

    def test_if_fsc_request_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.freischalt_code_request)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert isinstance(job_service.background_worker, BackgroundJobRq)
        assert issubclass(job_service.payload_type, FreischaltCodeRequestDto)
        assert issubclass(job_service.request_controller, UnlockCodeRequestController)

    def test_if_fsc_activate_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.freischalt_code_activate)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert isinstance(job_service.background_worker, BackgroundJobRq)
        assert issubclass(job_service.payload_type, FreischaltCodeActivateDto)
        assert issubclass(job_service.request_controller, UnlockCodeActivationRequestController)

    def test_if_fsc_revocate_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.freischalt_code_revocate)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert isinstance(job_service.background_worker, BackgroundJobRq)
        assert issubclass(job_service.payload_type, FreischaltCodeRevocateDto)
        assert issubclass(job_service.request_controller, UnlockCodeRevocationRequestController)

    def test_if_check_tax_number_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.check_tax_number)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert isinstance(job_service.background_worker, BackgroundJobRq)
        assert issubclass(job_service.payload_type, CheckTaxNumberDto)
        assert issubclass(job_service.request_controller, CheckTaxNumberRequestController)

    def test_if_send_est_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.send_est)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert isinstance(job_service.background_worker, BackgroundJobRq)
        assert issubclass(job_service.payload_type, TaxDeclarationDto)
        assert issubclass(job_service.request_controller, EstRequestController)
