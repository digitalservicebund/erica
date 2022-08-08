import uuid
from unittest.mock import MagicMock

import pytest

from erica.api.dto.response_dto import JobState
from erica.api.service.tax_number_validition_service import TaxNumberValidityService
from erica.domain.model.erica_request import EricaRequest, RequestType, Status


class TestTaxNumberValidityService:

    @pytest.mark.parametrize("status", [Status.new, Status.scheduled, Status.processing])
    def test_if_erica_request_found_and_not_finished_then_return_processing_response_dto(self, status):
        erica_request = EricaRequest(type=RequestType.check_tax_number, status=status,
                                     payload={},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = TaxNumberValidityService(service=mock_service).get_response_tax_number_validity("test")
        assert response.process_status == JobState.PROCESSING
        assert response.result is None
        assert response.error_code is None
        assert response.error_message is None

    def test_if_erica_request_found_and_failed_then_return_failed_response_dto(self):
        error_code = "1"
        error_message = "wingardium leviosa"
        erica_request = EricaRequest(type=RequestType.check_tax_number, status=Status.failed,
                                     payload={},
                                     error_code=error_code,
                                     error_message=error_message,
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = TaxNumberValidityService(service=mock_service).get_response_tax_number_validity("test")
        assert response.process_status == JobState.FAILURE
        assert response.error_code == error_code
        assert response.error_message == error_message
        assert response.result is None

    def test_if_erica_request_found_and_success_then_return_success_response_dto(self):
        is_valid = True
        erica_request = EricaRequest(type=RequestType.check_tax_number, status=Status.success,
                                     payload={},
                                     result={"is_valid": is_valid},
                                     request_id=uuid.uuid4(),
                                     creator_id="test")
        mock_get_request_by_request_id = MagicMock(return_value=erica_request)
        mock_service = MagicMock(get_request_by_request_id=mock_get_request_by_request_id)
        response = TaxNumberValidityService(service=mock_service).get_response_tax_number_validity("test")
        assert response.process_status == JobState.SUCCESS
        assert response.result.is_valid == is_valid
        assert response.error_code is None
        assert response.error_message is None
