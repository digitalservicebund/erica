import pytest

from erica.worker.jobs.freischaltcode_jobs import activate_freischalt_code, revocate_freischalt_code, \
    request_freischalt_code
from erica.shared.job_service.job_service_factory import get_job_service
from erica.worker.jobs.grundsteuer_jobs import send_grundsteuer
from erica.worker.jobs.tax_declaration_jobs import send_est
from erica.worker.jobs.tax_number_validation_jobs import check_tax_number
from erica.shared.payload.freischaltcode import FreischaltCodeRequestPayload, FreischaltCodeActivatePayload, \
    FreischaltCodeRevocatePayload
from erica.shared.model.base_domain_model import BasePayload
from erica.shared.model.erica_request import RequestType
from erica.shared.payload.tax_declaration import TaxDeclarationPayload
from erica.shared.payload.tax_number_validation import CheckTaxNumberPayload
from erica.api.dto.grundsteuer_dto import GrundsteuerPayload
from erica.worker.request_processing.requests_controller import UnlockCodeRevocationRequestController, \
    UnlockCodeRequestController, CheckTaxNumberRequestController, UnlockCodeActivationRequestController, \
    EstRequestController
from erica.shared.sqlalchemy.repositories.erica_request_repository import EricaRequestRepository
from erica.worker.request_processing.grundsteuer_request_controller import GrundsteuerRequestController


class TestJobServiceFactory:

    def test_if_unknown_dto_as_input_then_raise_not_implemented_error(self):
        class NotFoundDto(BasePayload):
            pass

        with pytest.raises(NotImplementedError):
            get_job_service(NotFoundDto)

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_fsc_request_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.freischalt_code_request)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert issubclass(job_service.payload_type, FreischaltCodeRequestPayload)
        assert issubclass(job_service.request_controller, UnlockCodeRequestController)
        assert job_service.job_method == request_freischalt_code

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_fsc_activate_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.freischalt_code_activate)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert issubclass(job_service.payload_type, FreischaltCodeActivatePayload)
        assert issubclass(job_service.request_controller, UnlockCodeActivationRequestController)
        assert job_service.job_method == activate_freischalt_code

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_fsc_revocate_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.freischalt_code_revocate)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert issubclass(job_service.payload_type, FreischaltCodeRevocatePayload)
        assert issubclass(job_service.request_controller, UnlockCodeRevocationRequestController)
        assert job_service.job_method == revocate_freischalt_code

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_check_tax_number_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.check_tax_number)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert issubclass(job_service.payload_type, CheckTaxNumberPayload)
        assert issubclass(job_service.request_controller, CheckTaxNumberRequestController)
        assert job_service.job_method == check_tax_number

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_send_est_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.send_est)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert issubclass(job_service.payload_type, TaxDeclarationPayload)
        assert issubclass(job_service.request_controller, EstRequestController)
        assert job_service.job_method == send_est

    @pytest.mark.usefixtures('fake_db_connection_in_settings')
    def test_if_send_grundsteuer_type_then_return_correctly_configured_service(self):
        job_service = get_job_service(RequestType.grundsteuer)

        assert isinstance(job_service.repository, EricaRequestRepository)
        assert issubclass(job_service.payload_type, GrundsteuerPayload)
        assert issubclass(job_service.request_controller, GrundsteuerRequestController)
        assert job_service.job_method == send_grundsteuer
