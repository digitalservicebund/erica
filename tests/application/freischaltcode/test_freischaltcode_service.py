import uuid
from unittest.mock import MagicMock

import pytest

from erica.application.shared.response_dto import JobState
from erica.application.freischaltcode.freischaltcode_service import FreischaltCodeService
from erica.domain.shared.erica_request import RequestType
from erica.domain.shared.status import Status
from erica.domain.erica_request.erica_request import EricaRequest


class TestFreischaltCodeService:

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing])
    def test_fsc_request_if_erica_request_found_and_not_finished_then_return_processing_response_dto(self, status):
        erica_request = EricaRequest(type=RequestType.freischalt_code_request, status=status,
                                     payload={},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_request("test")
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.error_message is None

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing])
    def test_fsc_activate_if_erica_request_found_and_not_finished_then_return_processing_response_dto(self, status):
        erica_request = EricaRequest(type=RequestType.freischalt_code_activate, status=status,
                                     payload={},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_activation("test")
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.error_message is None

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing])
    def test_fsc_revocate_if_erica_request_found_and_not_finished_then_return_processing_response_dto(self, status):
        erica_request = EricaRequest(type=RequestType.freischalt_code_revocate, status=status,
                                     payload={},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_revocation("test")
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.error_message is None

    def test_fsc_request_if_erica_request_found_and_failed_then_return_failed_response_dto(self):
        error_code = "1"
        error_message = "wingardium leviosa"
        erica_request = EricaRequest(type=RequestType.freischalt_code_request, status=Status.failed,
                                     payload={},
                                     error_code=error_code,
                                     error_message=error_message,
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_request("test")
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None

    def test_fsc_activate_if_erica_request_found_and_failed_then_return_failed_response_dto(self):
        error_code = "1"
        error_message = "wingardium leviosa"
        erica_request = EricaRequest(type=RequestType.freischalt_code_activate, status=Status.failed,
                                     payload={},
                                     error_code=error_code,
                                     error_message=error_message,
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_activation("test")
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None

    def test_fsc_revocate_if_erica_request_found_and_failed_then_return_failed_response_dto(self):
        error_code = "1"
        error_message = "wingardium leviosa"
        erica_request = EricaRequest(type=RequestType.freischalt_code_revocate, status=Status.failed,
                                     payload={},
                                     error_code=error_code,
                                     error_message=error_message,
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_revocation("test")
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None

    def test_fsc_request_if_erica_request_found_and_success_then_return_success_response_dto(self):
        tax_id_number = "test_idnr"
        elster_request_id = "test_elster_request_id"
        transferticket = "test_transferticket"
        erica_request = EricaRequest(type=RequestType.freischalt_code_request, status=Status.success,
                                     payload={"tax_id_number": tax_id_number},
                                     result={"elster_request_id": elster_request_id,
                                             "transferticket": transferticket},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_request("test")
        assert response.process_status == JobState.SUCCESS
        assert response.result.tax_id_number == tax_id_number
        assert response.result.elster_request_id == elster_request_id
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.error_message is None

    def test_fsc_activate_if_erica_request_found_and_success_then_return_success_response_dto(self):
        tax_id_number = "test_idnr"
        elster_request_id = "test_elster_request_id"
        transferticket = "test_transferticket"
        erica_request = EricaRequest(type=RequestType.freischalt_code_activate, status=Status.success,
                                     payload={"tax_id_number": tax_id_number},
                                     result={"elster_request_id": elster_request_id,
                                             "transferticket": transferticket},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_activation("test")
        assert response.process_status == JobState.SUCCESS
        assert response.result.tax_id_number == tax_id_number
        assert response.result.elster_request_id == elster_request_id
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.error_message is None

    def test_fsc_revocate_if_erica_request_found_and_success_then_return_success_response_dto(self):
        tax_id_number = "test_idnr"
        transferticket = "test_transferticket"
        erica_request = EricaRequest(type=RequestType.freischalt_code_revocate, status=Status.success,
                                     payload={"tax_id_number": tax_id_number},
                                     result={"transferticket": transferticket, "idnr": tax_id_number},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = FreischaltCodeService(service=mock_service).get_response_freischaltcode_revocation("test")
        assert response.process_status == JobState.SUCCESS
        assert response.result.tax_id_number == tax_id_number
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.error_message is None
