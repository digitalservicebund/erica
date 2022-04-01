import logging
from unittest.mock import MagicMock, patch, call, AsyncMock
from uuid import uuid4

import pytest

from erica.application.JobService.job_service import JobService
from erica.application.JobService.job_service_factory import get_job_service
from erica.application.tax_number_validation.jobs import check_tax_number
from erica.domain.Shared.EricaRequest import RequestType
from erica.domain.erica_request.erica_request import EricaRequest
from erica.domain.tax_number_validation.check_tax_number import CheckTaxNumberPayload, StateAbbreviation


class TestCheckTaxNumber:

    @pytest.mark.asyncio
    async def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.tax_number_validation.jobs.perform_job", AsyncMock()) as mock_perform_job:
            await check_tax_number(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        payload_type=mock_get_service().payload_type)]

    @pytest.mark.asyncio
    async def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.tax_number_validation.jobs.perform_job", AsyncMock()):
            await check_tax_number(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.check_tax_number)]

    @pytest.mark.asyncio
    async def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock(process=MagicMock(return_value={}))
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                background_worker=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=check_tax_number
            ))
        with patch("erica.application.JobService.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.erica_legacy.request_processing.requests_controller.CheckTaxNumberRequestController", mock_req_controller):
            await check_tax_number("1234")

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndCheckTaxNumber:

    @pytest.mark.asyncio
    @pytest.mark.usefixtures('async_fake_db_connection_with_erica_table_in_settings')
    async def test_if_entity_in_data_base_then_set_correct_result_in_database(self, standard_est_input_data):
        payload = CheckTaxNumberPayload(
            state_abbreviation=StateAbbreviation.bw,
            tax_number='04531972802')
        service = get_job_service(RequestType.check_tax_number)
        entity = service.repository.create(EricaRequest(
            request_id=uuid4(),
            payload=payload,
            creator_id="tests",
            type=RequestType.freischalt_code_revocate
        ))
        with patch('erica.erica_legacy.pyeric.pyeric_controller.CheckTaxNumberPyericController.get_eric_response',
                   MagicMock(return_value=True)):
            await check_tax_number(entity.request_id)

        updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'is_valid': True}