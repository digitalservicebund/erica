import uuid
from unittest.mock import MagicMock

import pytest

from erica.application.Shared.response_dto import JobState
from erica.application.tax_declaration.TaxDeclarationService import TaxDeclarationService
from erica.domain.Shared.EricaRequest import RequestType
from erica.domain.Shared.Status import Status
from erica.domain.erica_request.erica_request import EricaRequest


class TestTaxDeclarationService:

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing])
    def test_if_erica_request_found_and_not_finished_then_return_processing_response_dto(self, status):
        erica_request = EricaRequest(type=RequestType.send_est, status=status,
                                     payload={},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = TaxDeclarationService(service=mock_service).get_response_send_est("test")
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.errorMessage is None

    def test_if_erica_request_found_and_failed_then_return_failed_response_dto(self):
        error_code = "1"
        error_message = "wingardium leviosa"
        erica_request = EricaRequest(type=RequestType.send_est, status=Status.failed,
                                     payload={},
                                     error_code=error_code,
                                     error_message=error_message,
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = TaxDeclarationService(service=mock_service).get_response_send_est("test")
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.errorMessage == error_message
        assert response.result is None

    def test_if_erica_request_found_and_success_then_return_success_response_dto(self):
        pdf = "test_pdf"
        transferticket = "test_transferticket"
        erica_request = EricaRequest(type=RequestType.send_est, status=Status.success,
                                     payload={},
                                     result={"transferticket": transferticket, "pdf": pdf},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = TaxDeclarationService(service=mock_service).get_response_send_est("test")
        assert response.process_status == JobState.SUCCESS
        assert response.result.pdf == pdf
        assert response.result.transferticket == transferticket
        assert response.error_code is None
        assert response.errorMessage is None
