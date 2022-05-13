import logging
from datetime import date
from unittest.mock import patch, MagicMock, call, AsyncMock
from uuid import uuid4

import pytest

from erica.application.FreischaltCode.Jobs.jobs import request_freischalt_code, activate_freischalt_code, \
    revocate_freischalt_code
from erica.application.JobService.job_service import JobService
from erica.application.JobService.job_service_factory import get_job_service
from erica.domain.FreischaltCode.FreischaltCode import FreischaltCodeActivatePayload, FreischaltCodeRequestPayload, \
    FreischaltCodeRevocatePayload
from erica.domain.Shared.EricaRequest import RequestType
from erica.domain.erica_request.erica_request import EricaRequest
from erica.erica_legacy.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_antrag_id_from_xml, \
    get_transfer_ticket_from_xml
from erica.erica_legacy.pyeric.pyeric_response import PyericResponse
from tests.utils import read_text_from_sample


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
                                                        payload_type=mock_get_service().payload_type)]

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

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndRequestFreischaltcode:

    @pytest.mark.asyncio
    @pytest.mark.usefixtures('async_fake_db_connection_with_erica_table_in_settings')
    async def test_if_entity_in_data_base_then_set_correct_result_in_database(self):
        payload = FreischaltCodeRequestPayload(tax_id_number='04452397687', date_of_birth=date(1950, 8, 16))
        service = get_job_service(RequestType.freischalt_code_request)
        entity = service.repository.create(EricaRequest(
            request_id=uuid4(),
            payload=payload,
            creator_id="tests",
            type=RequestType.freischalt_code_request
        ))
        xml_string = read_text_from_sample('sample_vast_request_response.xml')
        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response',
                   MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string))):
            await request_freischalt_code(entity.request_id)

        updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'elster_request_id': get_antrag_id_from_xml(xml_string),
                                         'idnr': payload.tax_id_number,
                                         'transfer_ticket': get_transfer_ticket_from_xml(xml_string)}


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
                                                        payload_type=mock_get_service().payload_type)]

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

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndActivateFreischaltcode:

    @pytest.mark.asyncio
    @pytest.mark.usefixtures('async_fake_db_connection_with_erica_table_in_settings')
    async def test_if_entity_in_data_base_then_set_correct_result_in_database(self):
        payload = FreischaltCodeActivatePayload(tax_id_number='04452397687', freischalt_code='Alohomora', elster_request_id='br1272xf3i59m2323ft9qtk7iqzxzke4')
        service = get_job_service(RequestType.freischalt_code_activate)
        entity = service.repository.create(EricaRequest(
            request_id=uuid4(),
            payload=payload,
            creator_id="tests",
            type=RequestType.freischalt_code_activate
        ))
        xml_string = read_text_from_sample('sample_vast_activation_response.xml')
        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response',
                   MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string))):
            await activate_freischalt_code(entity.request_id)

        updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'elster_request_id': get_antrag_id_from_xml(xml_string),
                                         'idnr': payload.tax_id_number,
                                         'transfer_ticket': get_transfer_ticket_from_xml(xml_string)}


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
                                                        payload_type=mock_get_service().payload_type)]

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

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndRevocateFreischaltcode:

    @pytest.mark.asyncio
    @pytest.mark.usefixtures('async_fake_db_connection_with_erica_table_in_settings')
    async def test_if_entity_in_data_base_then_set_correct_result_in_database(self):
        payload = FreischaltCodeRevocatePayload(tax_id_number='04452397687', dob=date(1950, 8, 16), elster_request_id='br1272xf3i59m2323ft9qtk7iqzxzke4')
        service = get_job_service(RequestType.freischalt_code_revocate)
        entity = service.repository.create(EricaRequest(
            request_id=uuid4(),
            payload=payload,
            creator_id="tests",
            type=RequestType.freischalt_code_revocate
        ))
        xml_string = read_text_from_sample('sample_vast_revocation_response.xml')
        with patch('erica.erica_legacy.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response',
                   MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string))):
            await revocate_freischalt_code(entity.request_id)

        updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'elster_request_id': get_antrag_id_from_xml(xml_string),
                                         'transfer_ticket': get_transfer_ticket_from_xml(xml_string)}

