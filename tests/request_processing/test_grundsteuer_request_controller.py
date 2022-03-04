import base64
from unittest.mock import patch, MagicMock
from xml.etree import ElementTree

import pytest

from erica.pyeric.pyeric_response import PyericResponse
from erica.request_processing.grundsteuer_request_controller import GrundsteuerRequestController
from tests.samples.grundsteuer_sample_data import create_grundsteuer
from tests.utils import missing_cert, missing_pyeric_lib


@pytest.fixture
def valid_grundsteuer_request_controller():
    grundsteuer_input = create_grundsteuer()
    return GrundsteuerRequestController(grundsteuer_input)


class TestIsTestmerkerUsed:
    def test_returns_true(self, valid_grundsteuer_request_controller):
        result = valid_grundsteuer_request_controller._is_testmerker_used()
        assert result is True


@pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGenerateFullXml:
    def test_returns_valid_xml(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        try:
            ElementTree.fromstring(resulting_xml)
        except ElementTree.ParseError as e:
            return pytest.fail("Did not result in a valid xml: \n" + e.msg)

    def test_returned_xml_includes_transfer_header(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        assert "<TransferHeader" in resulting_xml

    def test_returned_xml_includes_nutzdaten(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        assert "<Nutzdaten" in resulting_xml

    def test_returned_xml_includes_nutzdaten_header(self, valid_grundsteuer_request_controller):
        resulting_xml = valid_grundsteuer_request_controller.generate_full_xml(use_testmerker=True)
        assert "<NutzdatenHeader" in resulting_xml


class TestGenerateJson:
    def test_result_includes_all_relevant_aspects(self, valid_grundsteuer_request_controller):
        valid_grundsteuer_request_controller.include_elster_responses = True
        example_pyeric_response = PyericResponse("eric response", "server response", "pdf content".encode())
        with patch('erica.request_processing.requests_controller.get_transfer_ticket_from_xml', MagicMock(return_value='transfer ticket')):
            result = valid_grundsteuer_request_controller.generate_json(example_pyeric_response)
            assert result['pdf'] == base64.b64encode("pdf content".encode())
            assert result['transfer_ticket'] == 'transfer ticket'
            assert result['eric_response'] == 'eric response'
            assert result['server_response'] == 'server response'
