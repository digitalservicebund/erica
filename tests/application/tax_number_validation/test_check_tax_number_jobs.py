import logging
from unittest.mock import MagicMock, patch, call, AsyncMock

import pytest

from erica.application.JobService.job_service import JobService
from erica.application.tax_number_validation.jobs import check_tax_number
from erica.domain.Shared.EricaRequest import RequestType


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
