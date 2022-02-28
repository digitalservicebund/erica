import copy
from unittest.mock import patch, MagicMock

import pytest as pytest

from erica.elster_xml.common.transfer_header import add_transfer_header
from erica.elster_xml.transfer_header_fields import TransferHeaderFields
from erica.pyeric.eric_errors import EricProcessNotSuccessful
from tests.utils import missing_cert, missing_pyeric_lib, remove_declaration_and_namespace


class TestGenerateTransferHeader:

    @pytest.fixture
    def correct_input_xml(self):
        with open('tests/samples/sample_vast_request.xml', 'r') as f:
            correct_input_xml_string = f.read()
            from xml.etree.ElementTree import tostring
            return tostring(remove_declaration_and_namespace(correct_input_xml_string)).decode()

    @pytest.fixture
    def incorrect_input_xml(self):
        return "<xml/>"

    @pytest.fixture
    def th_fields(self):
        return TransferHeaderFields(
            datenart='ESt',
            testmerker='700000004',
            herstellerId='74931',
            verfahren='ElsterErklaerung',
            datenLieferant='Softwaretester ERiC',
        )

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_correct_input_then_transfer_header_is_added_and_reference_unchanged(self, correct_input_xml, th_fields):
        input_xml_before_use = copy.deepcopy(correct_input_xml)

        result = add_transfer_header(correct_input_xml, th_fields)

        assert "TransferHeader" in result
        assert "<Testmerker>" + th_fields.testmerker + "</Testmerker>" in result
        assert "<DatenArt>" + th_fields.datenart + "</DatenArt>" in result
        assert "<HerstellerID>" + th_fields.herstellerId + "</HerstellerID>" in result
        assert "<DatenLieferant>" + th_fields.datenLieferant + "</DatenLieferant>" in result

        assert correct_input_xml == input_xml_before_use

    @pytest.mark.skipif(missing_cert(), reason="skipped because of missing cert.pfx; see pyeric/README.md")
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_if_incorrect_input_then_raise_not_successful_error(self, incorrect_input_xml, th_fields):
        with pytest.raises(EricProcessNotSuccessful):
            add_transfer_header(incorrect_input_xml, th_fields)

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_generate_transfer_header_calls_run_pyeric(self, th_fields):
        xml = "<xml/>"
        xml_with_th_binary = '<xml>This includes the transfer header.</xml>'.encode()
        with patch('erica.pyeric.eric.EricWrapper.create_th',
                   MagicMock(return_value=xml_with_th_binary)) as fun_create_th:
            add_transfer_header(xml, th_fields)

            fun_create_th.assert_called_with(xml,
                                             datenart=th_fields.datenart, testmerker=th_fields.testmerker,
                                             herstellerId=th_fields.herstellerId,
                                             verfahren=th_fields.verfahren,
                                             datenLieferant=th_fields.datenLieferant)

    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_generate_transfer_header_returns_xml_with_transfer_header(self, th_fields):
        xml = "<xml/>"
        xml_with_th_binary = '<xml>This includes the transfer header.</xml>'.encode()
        with patch('erica.pyeric.eric.EricWrapper.create_th',
                   MagicMock(return_value=xml_with_th_binary)):
            res = add_transfer_header(xml, th_fields)

            assert res == xml_with_th_binary.decode()
