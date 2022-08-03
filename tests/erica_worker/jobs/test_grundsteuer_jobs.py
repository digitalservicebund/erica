import base64
import logging
from unittest.mock import call, patch, MagicMock, AsyncMock
from uuid import uuid4

import pytest

from erica.erica_shared.job_service.job_service import JobService
from erica.erica_shared.job_service.job_service_factory import get_job_service
from erica.erica_worker.jobs.grundsteuer_jobs import send_grundsteuer
from erica.erica_shared.model.erica_request import EricaRequest, RequestType
from erica.erica_worker.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_transferticket_from_xml
from erica.erica_worker.pyeric.pyeric_response import PyericResponse
from erica.erica_shared.sqlalchemy.database import session_scope
from tests.erica_worker.samples.grundsteuer_sample_data import SampleGrundsteuerData
from tests.utils import read_text_from_sample


class TestGrundsteuerJob:

    def test_perform_job_called_with_correct_parameters(self):
        request_id = "1234"

        with patch("erica.erica_shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.erica_worker.jobs.grundsteuer_jobs.perform_job", AsyncMock()) as mock_perform_job:
            send_grundsteuer(request_id)

            assert mock_perform_job.mock_calls == [call(request_id=request_id,
                                                        repository=mock_get_service().repository,
                                                        service=mock_get_service(),
                                                        logger=logging.getLogger(),
                                                        payload_type=mock_get_service().payload_type)]

    def test_get_job_service_called_with_correct_param(self):
        request_id = "1234"

        with patch("erica.erica_shared.job_service.job_service_factory.get_job_service", MagicMock()) as mock_get_service, \
                patch("erica.erica_worker.jobs.grundsteuer_jobs.perform_job", AsyncMock()):
            send_grundsteuer(request_id)

            assert mock_get_service.mock_calls == [call(RequestType.grundsteuer)]

    def test_request_controller_process_called_with_correct_params(self):
        req_payload = SampleGrundsteuerData().parse()
        mock_req_controller = MagicMock()
        mock_get_service = MagicMock(
            return_value=JobService(
                job_repository=MagicMock(),
                payload_type=MagicMock(parse_obj=MagicMock(return_value=req_payload)),
                request_controller=mock_req_controller,
                job_method=send_grundsteuer
            ))
        with patch("erica.erica_shared.job_service.job_service_factory.get_job_service", mock_get_service), \
                patch(
                    "erica.erica_worker.request_processing.grundsteuer_request_controller.GrundsteuerRequestController", mock_req_controller):
            send_grundsteuer("1234")

            assert [call(req_payload, True), call().process()] in mock_req_controller.mock_calls


class TestIntegrationWithDatabaseAndGrundsteuerJob:

    @pytest.mark.usefixtures('fake_db_connection_with_erica_table_in_settings')
    def test_if_entity_in_data_base_then_set_correct_result_in_database(self, standard_est_input_data):
        payload = SampleGrundsteuerData().parse()
        response_pdf = b"This is the world we live in"
        expected_pdf = base64.b64encode(response_pdf).decode()
        # Necessary due to async db fixture. See fixture definition for details.
        with session_scope():
            service = get_job_service(RequestType.grundsteuer)
            entity = service.repository.create(EricaRequest(
                request_id=uuid4(),
                payload=payload,
                creator_id="tests",
                type=RequestType.grundsteuer
            ))
            xml_string = read_text_from_sample('sample_grundsteuer_response.xml')
            with patch('erica.erica_worker.pyeric.pyeric_controller.GrundsteuerPyericProcessController.get_eric_response',
                    MagicMock(return_value=PyericResponse(eric_response="eric_response", server_response=xml_string, pdf=response_pdf))):
                send_grundsteuer(entity.request_id)

            updated_entity = service.repository.get_by_job_request_id(entity.request_id)

        assert updated_entity.result == {'transferticket': get_transferticket_from_xml(xml_string),
                                         'pdf': expected_pdf}
