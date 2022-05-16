import uuid
from unittest.mock import MagicMock, Mock, patch

import pytest

from erica import app
from erica.api.v2.endpoints.est import send_est, get_send_est_job
from erica.api.v2.endpoints.fsc import request_fsc, get_fsc_request_job, activate_fsc, get_fsc_activation_job, \
    revocate_fsc, get_fsc_revocation_job
from erica.api.v2.endpoints.grundsteuer import send_grundsteuer, get_grundsteuer_job
from erica.api.v2.endpoints.tax import is_valid_tax_number, get_valid_tax_number_job
from erica.application.FreischaltCode.FreischaltCodeService import FreischaltCodeService
from erica.application.JobService.job_service import JobService
from erica.application.Shared.response_dto import JobState
from erica.application.erica_request.erica_request import EricaRequestDto
from erica.application.grundsteuer.GrundsteuerService import GrundsteuerService
from erica.application.tax_declaration.TaxDeclarationService import TaxDeclarationService
from erica.application.tax_number_validation.TaxNumberValidityService import TaxNumberValidityService
from erica.domain.Shared.EricaRequest import RequestType
from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest
from tests.application.job_service.test_job_service import MockEricaRequestRepository, MockRequestController, MockDto, \
    PickableMock
from tests.utils import create_unlock_code_request, \
    create_unlock_code_activation, create_unlock_code_revocation, create_tax_number_validity, create_send_est, \
    get_job_service_patch_string, create_send_grundsteuer


@pytest.mark.asyncio
@pytest.mark.parametrize("api_method, input_data, request_type, endpoint_to_patch, expected_location",
                         [(request_fsc, create_unlock_code_request(), RequestType.freischalt_code_request, "fsc",
                           "get_fsc_request_job"),
                          (activate_fsc, create_unlock_code_activation(), RequestType.freischalt_code_activate, "fsc",
                           "get_fsc_activation_job"),
                          (revocate_fsc, create_unlock_code_revocation(), RequestType.freischalt_code_revocate, "fsc",
                           "get_fsc_revocation_job"),
                          (is_valid_tax_number, create_tax_number_validity(), RequestType.check_tax_number, "tax",
                           "get_valid_tax_number_job"),
                          (send_est, create_send_est(), RequestType.send_est, "est", "get_send_est_job"),
                          (send_grundsteuer, create_send_grundsteuer(), RequestType.grundsteuer, "grundsteuer",
                           "get_grundsteuer_job")],
                         ids=["request_fsc", "activate_fsc", "revocate_fsc", "is_valid_tax_number", "send_est",
                              "grundsteuer"])
async def test_if_post_job_returns_location_with_uuid(api_method, input_data, request_type, endpoint_to_patch,
                                                      expected_location):
    request_id = uuid.uuid4()
    job_service_mock = JobService(job_repository=MockEricaRequestRepository(), background_worker=MagicMock(),
                                  request_controller=MockRequestController, payload_type=MockDto,
                                  job_method=PickableMock())
    job_service_mock.add_to_queue = Mock(
        return_value=EricaRequestDto(type=request_type, status=Status.new, payload="{}",
                                     request_id=request_id))
    mock_url = app.url_path_for(expected_location, request_id=str(request_id))
    mock_request_object = MagicMock(url_for=MagicMock(return_value=str(mock_url)), base_url="lorem")
    with patch(get_job_service_patch_string(endpoint_to_patch), MagicMock(return_value=job_service_mock)):
        response = await api_method(input_data, mock_request_object)
        assert response.headers['Location'] == mock_url


@pytest.mark.asyncio
@pytest.mark.parametrize("api_method, request_type", [(get_fsc_request_job, RequestType.freischalt_code_request),
                                                      (get_fsc_activation_job, RequestType.freischalt_code_activate)],
                         ids=["request_fsc", "activate_fsc"])
async def test_if_get_fsc_request_or_activation_job_returns_success_status_with_result(api_method, request_type):
    request_id = uuid.uuid4()
    tax_id_number = "test_idnr"
    elster_request_id = "test_elster_request_id"
    transferticket = "test_transferticket"
    erica_request = EricaRequest(type=request_type, status=Status.success,
                                 payload={"tax_id_number": tax_id_number},
                                 result={"elster_request_id": elster_request_id,
                                         "transferticket": transferticket},
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.fsc.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = FreischaltCodeService(service=mock_service)
        response = await api_method(request_id)
        assert response.process_status == JobState.SUCCESS
        assert response.result.idnr == tax_id_number
        assert response.result.elster_request_id == elster_request_id
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.error_message is None


@pytest.mark.asyncio
async def test_if_get_fsc_revocation_job_returns_success_status_with_result():
    request_id = uuid.uuid4()
    tax_id_number = "test_idnr"
    transferticket = "test_transferticket"
    erica_request = EricaRequest(type=RequestType.freischalt_code_revocate, status=Status.success,
                                 payload={"tax_id_number": tax_id_number},
                                 result={"transferticket": transferticket, "idnr": tax_id_number},
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.fsc.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = FreischaltCodeService(service=mock_service)
        response = await get_fsc_revocation_job(request_id)
        assert response.process_status == JobState.SUCCESS
        assert response.result.idnr == tax_id_number
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.error_message is None


@pytest.mark.asyncio
async def test_if_get_tax_validity_job_returns_success_status_with_result():
    request_id = uuid.uuid4()
    is_valid = True
    erica_request = EricaRequest(type=RequestType.check_tax_number, status=Status.success,
                                 payload={},
                                 result={"is_valid": is_valid},
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.tax.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = TaxNumberValidityService(service=mock_service)
        response = await get_valid_tax_number_job(request_id)
        assert response.process_status == JobState.SUCCESS
        assert response.result.is_valid == is_valid
        assert response.error_code is None
        assert response.error_message is None


@pytest.mark.asyncio
async def test_if_get_send_est_job_returns_success_status_with_result():
    request_id = uuid.uuid4()
    pdf = "test_pdf"
    transferticket = "test_transferticket"
    erica_request = EricaRequest(type=RequestType.send_est, status=Status.success,
                                 payload={},
                                 result={"transferticket": transferticket, "pdf": pdf},
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.est.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = TaxDeclarationService(service=mock_service)
        response = await get_send_est_job(request_id)
        assert response.process_status == JobState.SUCCESS
        assert response.result.pdf == pdf
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.error_message is None


@pytest.mark.asyncio
async def test_if_get_grundsteuer_job_returns_success_status_with_result():
    request_id = uuid.uuid4()
    pdf = "test_pdf"
    transferticket = "test_transferticket"
    erica_request = EricaRequest(type=RequestType.grundsteuer, status=Status.success,
                                 payload={},
                                 result={"transferticket": transferticket, "pdf": pdf},
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.grundsteuer.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = GrundsteuerService(service=mock_service)
        response = await get_grundsteuer_job(request_id)
        assert response.process_status == JobState.SUCCESS
        assert response.result.pdf == pdf
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.error_message is None


@pytest.mark.asyncio
@pytest.mark.parametrize("api_method, request_type",
                         [(get_fsc_request_job, RequestType.freischalt_code_request),
                          (get_fsc_activation_job, RequestType.freischalt_code_activate),
                          (get_fsc_revocation_job, RequestType.freischalt_code_revocate)],
                         ids=["request_fsc", "activate_fsc", "revocate_fsc"])
async def test_if_get_fsc_job_returns_failure_status(api_method, request_type):
    request_id = uuid.uuid4()
    error_code = "1"
    error_message = "wingardium leviosa"
    erica_request = EricaRequest(type=request_type, status=Status.failed,
                                 error_code=error_code,
                                 error_message=error_message,
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.fsc.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = FreischaltCodeService(service=mock_service)
        response = await api_method(request_id)
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None


@pytest.mark.asyncio
async def test_if_get_tax_validity_job_returns_failure_status():
    request_id = uuid.uuid4()
    error_code = "1"
    error_message = "wingardium leviosa"
    erica_request = EricaRequest(type=RequestType.check_tax_number, status=Status.failed,
                                 error_code=error_code,
                                 error_message=error_message,
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.tax.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = TaxNumberValidityService(service=mock_service)
        response = await get_valid_tax_number_job(request_id)
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None


@pytest.mark.asyncio
async def test_if_get_est_job_returns_failure_status():
    request_id = uuid.uuid4()
    error_code = "1"
    error_message = "wingardium leviosa"
    erica_request = EricaRequest(type=RequestType.send_est, status=Status.failed,
                                 error_code=error_code,
                                 error_message=error_message,
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.est.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = TaxDeclarationService(service=mock_service)
        response = await get_send_est_job(request_id)
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None


@pytest.mark.asyncio
async def test_if_get_grundsteuer_job_returns_failure_status():
    request_id = uuid.uuid4()
    error_code = "1"
    error_message = "wingardium leviosa"
    erica_request = EricaRequest(type=RequestType.grundsteuer, status=Status.failed,
                                 error_code=error_code,
                                 error_message=error_message,
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.grundsteuer.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = GrundsteuerService(service=mock_service)
        response = await get_grundsteuer_job(request_id)
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_job_state", [Status.new, Status.scheduled, Status.processing])
@pytest.mark.parametrize("api_method, request_type",
                         [(get_fsc_request_job, RequestType.freischalt_code_request),
                          (get_fsc_activation_job, RequestType.freischalt_code_activate),
                          (get_fsc_revocation_job, RequestType.freischalt_code_revocate)],
                         ids=["request_fsc", "activate_fsc", "revocate_fsc"])
async def test_if_get_fsc_job_returns_processing_status(mock_job_state, api_method, request_type):
    request_id = uuid.uuid4()
    erica_request = EricaRequest(type=request_type, status=mock_job_state,
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.fsc.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = FreischaltCodeService(service=mock_service)
        response = await api_method(request_id)
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.error_message is None


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_job_state", [Status.new, Status.scheduled, Status.processing])
@pytest.mark.parametrize("api_method, request_type", [(get_valid_tax_number_job, RequestType.check_tax_number)])
async def test_if_get_tax_validity_job_returns_processing_status(mock_job_state, api_method, request_type):
    request_id = uuid.uuid4()
    erica_request = EricaRequest(type=request_type, status=mock_job_state,
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.tax.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = TaxNumberValidityService(service=mock_service)
        response = await api_method(request_id)
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.error_message is None


@pytest.mark.asyncio
@pytest.mark.parametrize("mock_job_state", [Status.new, Status.scheduled, Status.processing])
@pytest.mark.parametrize("api_method, request_type", [(get_send_est_job, RequestType.send_est)])
async def test_if_get_est_job_returns_processing_status(mock_job_state, api_method, request_type):
    request_id = uuid.uuid4()
    erica_request = EricaRequest(type=request_type, status=mock_job_state,
                                 request_id=request_id, creator_id="test")
    with patch("erica.api.v2.endpoints.est.get_service", MagicMock()) as get_service_mock:
        mock_service = MagicMock(get_request_by_request_id=MagicMock(return_value=erica_request))
        get_service_mock.return_value = TaxDeclarationService(service=mock_service)
        response = await api_method(request_id)
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.error_message is None
