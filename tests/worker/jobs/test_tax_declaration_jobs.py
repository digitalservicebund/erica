import base64
import logging
from unittest.mock import call, patch, MagicMock, AsyncMock
from uuid import uuid4

import pytest

from erica.job_service.job_service import JobService
from erica.job_service.job_service_factory import get_job_service
from erica.worker.jobs.tax_declaration_jobs import send_est
from erica.domain.payload.tax_declaration import TaxDeclarationPayload
from erica.domain.model.erica_request import EricaRequest, RequestType
from erica.worker.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_transferticket_from_xml
from erica.worker.pyeric.pyeric_response import PyericResponse
from erica.worker.request_processing.erica_input.v1.erica_input import MetaDataEst
from erica.domain.sqlalchemy.database import session_scope
from worker.utils import TEST_EST_VERANLAGUNGSJAHR
from utils import read_text_from_sample


class TestTaxDeclarationJob:

    def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.tax_declaration_jobs.perform_job", AsyncMock()) as mock_perform_job:
            send_est(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        payload_type=mock_get_service().payload_type)]

    def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.worker.jobs.tax_declaration_jobs.perform_job", AsyncMock()):
            send_est(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.send_est)]

    def test_request_controller_process_called_with_correct_params(self):
        req_payload = {"name": "Leon, der Profi"}
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=send_est
            ))
        with patch("erica.job_service.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.worker.request_processing.requests_controller.EstRequestController", mock_req_controller):
            send_est("1234")

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndTaxDeclarationJob:

    @pytest.mark.usefixtures('fake_db_connection_with_erica_table_in_settings')
    def test_if_entity_in_data_base_then_set_correct_result_in_database(self, standard_est_input_data):
        payload = TaxDeclarationPayload(
            est_data=standard_est_input_data,
            meta_data=MetaDataEst(year=TEST_EST_VERANLAGUNGSJAHR))
        response_pdf = b"This is the world we live in"
        expected_pdf = base64.b64encode(response_pdf).decode()
        # Necessary due to async db fixture. See fixture definition for details.
        with session_scope():
            service = get_job_service(RequestType.send_est)
            entity = service.repository.create(EricaRequest(
                request_id=uuid4(),
                payload=payload,
                creator_id="tests",
                type=RequestType.freischalt_code_revocate
            ))
            xml_string = read_text_from_sample('sample_est_response_server.xml')
            with patch('erica.worker.pyeric.pyeric_controller.EstPyericProcessController.get_eric_response',
                    MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string, pdf=response_pdf))):
                send_est(entity.request_id)

            updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'transferticket': get_transferticket_from_xml(xml_string),
                                         'pdf': expected_pdf}
