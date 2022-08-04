import logging
from datetime import date
from unittest.mock import patch, MagicMock, call, AsyncMock
from uuid import uuid4

import pytest

from erica.worker.jobs.freischaltcode_jobs import request_freischalt_code, activate_freischalt_code, \
    revocate_freischalt_code
from erica.shared.job_service.job_service import JobService
from erica.shared.job_service.job_service_factory import get_job_service
from erica.shared.payload.freischaltcode import FreischaltCodeActivatePayload, FreischaltCodeRequestPayload, \
    FreischaltCodeRevocatePayload
from erica.shared.model.erica_request import EricaRequest, RequestType
from erica.worker.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_antrag_id_from_xml, \
    get_transferticket_from_xml
from erica.worker.pyeric.pyeric_response import PyericResponse
from erica.shared.sqlalchemy.database import session_scope
from tests.utils import read_text_from_sample


class TestRequestFreischaltcode:

    def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.freischaltcode_jobs.perform_job", AsyncMock()) as mock_perform_job:
            request_freischalt_code(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        payload_type=mock_get_service().payload_type)]

    def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.freischaltcode_jobs.perform_job", AsyncMock()):
            request_freischalt_code(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.freischalt_code_request)]

    def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=request_freischalt_code
            ))
        with patch("erica.shared.job_service.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.worker.request_processing.requests_controller.UnlockCodeRequestController", mock_req_controller):
            request_freischalt_code("1234")

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndRequestFreischaltcode:

    @pytest.mark.usefixtures('fake_db_connection_with_erica_table_in_settings')
    def test_if_entity_in_data_base_then_set_correct_result_in_database(self):
        # Necessary due to async db fixture. See fixture definition for details.
        with session_scope():
            payload = FreischaltCodeRequestPayload(tax_id_number='04452397687', date_of_birth=date(1950, 8, 16))
            service = get_job_service(RequestType.freischalt_code_request)
            entity = service.repository.create(EricaRequest(
                request_id=uuid4(),
                payload=payload,
                creator_id="tests",
                type=RequestType.freischalt_code_request
            ))
            xml_string = read_text_from_sample('sample_vast_request_response.xml')
            with patch('erica.worker.pyeric.pyeric_controller.UnlockCodeRequestPyericProcessController.get_eric_response',
                    MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string))):
                request_freischalt_code(entity.request_id)

            updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'elster_request_id': get_antrag_id_from_xml(xml_string),
                                         'idnr': payload.tax_id_number,
                                         'transferticket': get_transferticket_from_xml(xml_string)}


class TestActivateFreischaltcode:

    def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.freischaltcode_jobs.perform_job", AsyncMock()) as mock_perform_job:
            activate_freischalt_code(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        payload_type=mock_get_service().payload_type)]

    def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.freischaltcode_jobs.perform_job", AsyncMock()):
            activate_freischalt_code(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.freischalt_code_activate)]

    def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=activate_freischalt_code
            ))
        with patch("erica.shared.job_service.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.worker.request_processing.requests_controller.UnlockCodeActivationRequestController", mock_req_controller):
            activate_freischalt_code("1234")

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndActivateFreischaltcode:

    @pytest.mark.usefixtures('fake_db_connection_with_erica_table_in_settings')
    def test_if_entity_in_data_base_then_set_correct_result_in_database(self):
        payload = FreischaltCodeActivatePayload(tax_id_number='04452397687', freischalt_code='Alohomora', elster_request_id='br1272xf3i59m2323ft9qtk7iqzxzke4')
        # Necessary due to async db fixture. See fixture definition for details.
        with session_scope():
            service = get_job_service(RequestType.freischalt_code_activate)
            entity = service.repository.create(EricaRequest(
                request_id=uuid4(),
                payload=payload,
                creator_id="tests",
                type=RequestType.freischalt_code_activate
            ))
            xml_string = read_text_from_sample('sample_vast_activation_response.xml')
            with patch('erica.worker.pyeric.pyeric_controller.UnlockCodeActivationPyericProcessController.get_eric_response',
                    MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string))):
                activate_freischalt_code(entity.request_id)

            updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'elster_request_id': get_antrag_id_from_xml(xml_string),
                                         'idnr': payload.tax_id_number,
                                         'transferticket': get_transferticket_from_xml(xml_string)}


class TestRevocateFreischaltcode:

    def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.freischaltcode_jobs.perform_job", AsyncMock()) as mock_perform_job:
            revocate_freischalt_code(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        payload_type=mock_get_service().payload_type)]

    async def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.freischaltcode_jobs.perform_job", AsyncMock()):
            revocate_freischalt_code(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.freischalt_code_revocate)]

    def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=revocate_freischalt_code
            ))
        with patch("erica.shared.job_service.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.worker.request_processing.requests_controller.UnlockCodeRevocationRequestController", mock_req_controller):
            revocate_freischalt_code("1234")

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndRevocateFreischaltcode:

    @pytest.mark.usefixtures('fake_db_connection_with_erica_table_in_settings')
    def test_if_entity_in_data_base_then_set_correct_result_in_database(self):
        # Necessary due to async db fixture. See fixture definition for details.
        with session_scope():
            payload = FreischaltCodeRevocatePayload(tax_id_number='04452397687', dob=date(1950, 8, 16), elster_request_id='br1272xf3i59m2323ft9qtk7iqzxzke4')
            service = get_job_service(RequestType.freischalt_code_revocate)
            entity = service.repository.create(EricaRequest(
                request_id=uuid4(),
                payload=payload,
                creator_id="tests",
                type=RequestType.freischalt_code_revocate
            ))
            xml_string = read_text_from_sample('sample_vast_revocation_response.xml')
            with patch('erica.worker.pyeric.pyeric_controller.UnlockCodeRevocationPyericProcessController.get_eric_response',
                    MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string))):
                revocate_freischalt_code(entity.request_id)

            updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'elster_request_id': get_antrag_id_from_xml(xml_string),
                                         'transferticket': get_transferticket_from_xml(xml_string)}

