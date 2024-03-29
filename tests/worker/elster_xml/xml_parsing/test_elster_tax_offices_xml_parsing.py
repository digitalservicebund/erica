import unittest

from erica.worker.elster_xml.xml_parsing.elster_specifics_xml_parsing import get_state_ids, get_tax_offices, \
    get_antrag_id_from_xml, get_idnr_from_xml, get_transferticket_from_xml, get_address_from_xml, \
    get_relevant_beleg_ids
from worker.utils import replace_text_in_xml
from utils import read_text_from_sample


class TestGetstateIds(unittest.TestCase):

    def test_if_valid_xml_then_correct_state_ids_are_extracted(self):
        expected_state_ids = [{'id': '28', 'name': 'Baden-Württemberg'},
                                {'id': '91', 'name': 'Bayern (Zuständigkeit LfSt - München)'},
                                {'id': '92', 'name': 'Bayern (Zuständigkeit LfSt - Nürnberg)'},
                                {'id': '11', 'name': 'Berlin'}]
        state_list_xml = read_text_from_sample('sample_state_list.xml', 'r')
        state_ids = get_state_ids(state_list_xml)
        self.assertEqual(expected_state_ids, state_ids)


class TestGetTaxOffices(unittest.TestCase):

    def test_if_valid_xml_then_correct_state_ids_are_extracted(self):
        expected_tax_offices = [{'bufa_nr': '2801', 'name': 'Finanzamt Offenburg Außenstelle Achern'},
                                {'bufa_nr': '2804', 'name': 'Finanzamt Villingen-Schwenningen Außenstelle Donaueschingen'},
                                {'bufa_nr': '2887', 'name': 'Finanzamt Überlingen (Bodensee)'},
                                {'bufa_nr': '2806', 'name': 'Finanzamt Freiburg-Stadt'},
                                {'bufa_nr': '2884', 'name': 'Finanzamt Schwäbisch Hall'}]

        tax_offices_xml = read_text_from_sample('sample_tax_offices.xml', 'r')
        tax_offices = get_tax_offices(tax_offices_xml)
        self.assertEqual(expected_tax_offices, tax_offices)


class TestAntragIdFromXml(unittest.TestCase):

    def test_antrag_element_is_returned_correctly(self):
        xml_string = read_text_from_sample('sample_vast_request_response.xml')
        antrag_id = get_antrag_id_from_xml(xml_string)
        self.assertEqual(antrag_id, 'br12701v299sh650fgwcn0c31z2k0xrb')


class TestIdNrFromXml(unittest.TestCase):
    def test_idnr_element_is_returned_correctly(self):
        xml_string = read_text_from_sample('sample_vast_request_response.xml')
        idnr = get_idnr_from_xml(xml_string)
        self.assertEqual(idnr, '04452397687')


class TestTransferticketFromXml(unittest.TestCase):
    def test_if_correct_server_response_then_return_correct_transferticket_value(self):
        expected_transferticket = 'Transferiates'
        xml_string = replace_text_in_xml(read_text_from_sample('sample_vast_request_response.xml'), 'TransferTicket', expected_transferticket)
        actual_transferticket = get_transferticket_from_xml(xml_string)
        self.assertEqual(expected_transferticket, actual_transferticket)


class TestAddressFromXml(unittest.TestCase):
    def test_if_correct_server_response_then_return_correct_transferticket_value(self):
        import html
        expected_address = html.unescape('<AdrKette>'
                                         '<StrAdr>'
                                         '<Str>&#220;xh&#228;&#252;&#228;&#246;-&#225;&#238;-&#255;&#241;-&#197;-Stra'
                                         '&#223;e</Str> '
                                         '<HausNr>1101</HausNr><Plz>34125</Plz><Ort>Kassel</Ort>'
                                         '</StrAdr>'
                                         '</AdrKette>').encode()
        actual_address = get_address_from_xml(read_text_from_sample('sample_beleg_address_response.xml'))
        self.assertEqual("".join(expected_address.decode().split()), "".join(actual_address.decode().split()))


class TestGetRelevantBelegIds(unittest.TestCase):
    def test_get_relevant_beleg_ids_and_idnr_returns_correct_beleg_ids_for_one_beleg_type(self):
        beleg_ids = get_relevant_beleg_ids(read_text_from_sample('sample_beleg_id_response.xml'), ['VaSt_RBM'])

        self.assertEqual(['vb3077iudj6nrd6h5istk3c3mzbbi88r'],  # only one RBM element
                         beleg_ids)

    def test_get_relevant_beleg_ids_and_idnr_returns_correct_beleg_ids_for_multiple_beleg_types(self):
        beleg_ids = get_relevant_beleg_ids(read_text_from_sample('sample_beleg_id_response.xml'), ['VaSt_RBM', 'VaSt_Pers1'])

        self.assertEqual(['vb3077iudj6nrd6h5istk3c3mzbbi88r', 'vg3071ovc201t97gdvyy1851qrutaheh'],
                         beleg_ids)