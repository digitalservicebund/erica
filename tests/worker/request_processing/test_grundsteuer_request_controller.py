import base64
import json
from unittest.mock import patch, MagicMock
from xml.etree import ElementTree

import pytest
from xmldiff import main

from erica.config import get_settings
from erica.worker.request_processing.grundsteuer_request_controller import GrundsteuerRequestController
from erica.worker.pyeric.pyeric_response import PyericResponse
from erica.api.dto.grundsteuer_dto import GrundsteuerPayload
from worker.samples.grundsteuer_sample_data import SampleGrundsteuerData
from worker.utils import missing_cert, missing_pyeric_lib
from utils import read_text_from_sample


@pytest.fixture
def valid_grundsteuer_request_controller():
    grundsteuer_input = SampleGrundsteuerData().parse()
    return GrundsteuerRequestController(grundsteuer_input)


class TestIsTestmerkerUsed:

    def test_if_tax_id_number_test_tax_id_then_returns_true(self, valid_grundsteuer_request_controller):
        valid_grundsteuer_request_controller.input_data.eigentuemer.person[0].steuer_id = "04452397687"
        result = valid_grundsteuer_request_controller._is_testmerker_used()
        assert result is True

    def test_if_tax_id_number_no_test_tax_id_then_returns_false(self, valid_grundsteuer_request_controller):
        valid_grundsteuer_request_controller.input_data.eigentuemer.person[0].steuer_id = "43865766025"
        result = valid_grundsteuer_request_controller._is_testmerker_used()
        assert result is False

    def test_if_no_tax_id_and_flag_set_then_returns_true(self, valid_grundsteuer_request_controller):
        orig_flag = get_settings().use_testmerker
        try:
            get_settings().use_testmerker = True
            valid_grundsteuer_request_controller.input_data.eigentuemer.person[0].steuer_id = None
            result = valid_grundsteuer_request_controller._is_testmerker_used()
            assert result is True
        finally:
            get_settings().use_testmerker = orig_flag

    def test_if_no_tax_id_and_flag_not_set_then_returns_false(self, valid_grundsteuer_request_controller):
        orig_flag = get_settings().use_testmerker
        try:
            get_settings().use_testmerker = False
            valid_grundsteuer_request_controller.input_data.eigentuemer.person[0].steuer_id = None
            result = valid_grundsteuer_request_controller._is_testmerker_used()
            assert result is False
        finally:
            get_settings().use_testmerker = orig_flag


@pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGenerateFullXml:
    def test_returns_valid_xml(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        ElementTree.fromstring(resulting_xml)

    def test_returned_xml_includes_transfer_header(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        assert "<TransferHeader" in resulting_xml

    def test_returned_xml_includes_nutzdaten(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        assert "<Nutzdaten" in resulting_xml

    def test_returned_xml_includes_nutzdaten_header(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        assert "<NutzdatenHeader" in resulting_xml

    def test_returns_full_expected_xml_for_given_input(self):
        payload = json.loads(read_text_from_sample('grundsteuer_sample_input.json'))
        parsed_input = GrundsteuerPayload.parse_obj(payload)
        request_controller = GrundsteuerRequestController(parsed_input)
        resulting_xml = request_controller.generate_full_xml(use_testmerker=True)
        expected_xml = read_text_from_sample('grundsteuer_sample_xml.xml')
        diff = main.diff_texts(bytes(bytearray(resulting_xml, "utf8")),
                               expected_xml.encode())
        assert diff == []

    def test_returns_full_expected_xml_for_given_input_bruchteilsgemeinschaft(self):
        with open('tests/worker/samples/grundsteuer_sample_input_bruchteilsgemeinschaft.json') as json_file:
            payload = json.loads(json_file.read())
            parsed_input = GrundsteuerPayload.parse_obj(payload)
            request_controller = GrundsteuerRequestController(parsed_input)
            resulting_xml = request_controller.generate_full_xml(use_testmerker=True)
            with open('tests/worker/samples/grundsteuer_sample_xml_bruchteilsgemeinschaft.xml') as f:
                expected_xml = f.read()
                diff = main.diff_texts(bytes(bytearray(resulting_xml, "utf8")),
                                       expected_xml.encode())
                assert diff == []


class TestGenerateJson:
    def test_result_includes_all_relevant_aspects(self, valid_grundsteuer_request_controller):
        valid_grundsteuer_request_controller.include_elster_responses = True
        example_pyeric_response = PyericResponse("eric response", "server response", "pdf content".encode())
        with patch('erica.worker.request_processing.requests_controller.get_transferticket_from_xml',
                   MagicMock(return_value='transferticket')):
            result = valid_grundsteuer_request_controller.generate_json(example_pyeric_response)
            assert result['pdf'] == base64.b64encode(b"pdf content").decode('utf-8')
            assert result['transferticket'] == 'transferticket'
            assert result['eric_response'] == 'eric response'
            assert result['server_response'] == 'server response'
