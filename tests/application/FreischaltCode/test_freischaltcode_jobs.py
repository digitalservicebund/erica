import logging
from unittest.mock import patch, MagicMock, call, AsyncMock

import pytest

from erica.application.FreischaltCode.Jobs.jobs import request_freischalt_code, activate_freischalt_code, \
    revocate_freischalt_code
from erica.application.JobService.job_service import JobService
from erica.domain.Shared.EricaAuftrag import RequestType


class TestRequestFreischaltcode:

    @pytest.mark.asyncio
    async def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.FreischaltCode.Jobs.jobs.perform_job", AsyncMock()) as mock_perform_job:
            await request_freischalt_code(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        dto=mock_get_service().payload_type)]

    @pytest.mark.asyncio
    async def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.FreischaltCode.Jobs.jobs.perform_job", AsyncMock()):
            await request_freischalt_code(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.freischalt_code_request)]

    @pytest.mark.asyncio
    async def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                background_worker=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=request_freischalt_code
            ))
        with patch("erica.application.JobService.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.erica_legacy.request_processing.requests_controller.UnlockCodeRequestController", mock_req_controller):
            await request_freischalt_code("1234")

            assert mock_req_controller.mock_calls == [call(req_payload, True), call().process()]


class TestActivateFreischaltcode:

    @pytest.mark.asyncio
    async def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.FreischaltCode.Jobs.jobs.perform_job", AsyncMock()) as mock_perform_job:
            await activate_freischalt_code(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        dto=mock_get_service().payload_type)]

    @pytest.mark.asyncio
    async def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.FreischaltCode.Jobs.jobs.perform_job", AsyncMock()):
            await activate_freischalt_code(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.freischalt_code_activate)]

    @pytest.mark.asyncio
    async def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                background_worker=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=activate_freischalt_code
            ))
        with patch("erica.application.JobService.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.erica_legacy.request_processing.requests_controller.UnlockCodeActivationRequestController", mock_req_controller):
            await activate_freischalt_code("1234")

            assert mock_req_controller.mock_calls == [call(req_payload, True), call().process()]


class TestRevocateFreischaltcode:

    @pytest.mark.asyncio
    async def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.FreischaltCode.Jobs.jobs.perform_job", AsyncMock()) as mock_perform_job:
            await revocate_freischalt_code(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        dto=mock_get_service().payload_type)]

    @pytest.mark.asyncio
    async def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.application.JobService.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.application.FreischaltCode.Jobs.jobs.perform_job", AsyncMock()):
            await revocate_freischalt_code(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.freischalt_code_revocate)]

    @pytest.mark.asyncio
    async def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                background_worker=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=revocate_freischalt_code
            ))
        with patch("erica.application.JobService.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.erica_legacy.request_processing.requests_controller.UnlockCodeRevocationRequestController", mock_req_controller):
            await revocate_freischalt_code("1234")

            assert mock_req_controller.mock_calls == [call(req_payload, True), call().process()]
