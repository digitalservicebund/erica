from xml.etree import ElementTree

import pytest

from erica.worker.elster_xml.common.basic_xml_data_representation import EEmpfaenger, ENutzdatenHeader, ENutzdaten, \
    ENutzdatenblock, EDatenTeil, EElster, EXml, construct_basic_xml_data_representation
from erica.worker.elster_xml.common.xml_conversion import convert_object_to_xml


@pytest.fixture
def nutzdaten():
    return ENutzdaten()


@pytest.fixture
def default_basic_xml_construction_args(nutzdaten):
    return "ID", "TEXT", nutzdaten, "VERSION", "TICKET"


class TestEEmpfaenger:
    def test_attributes_set_correctly(self):
        resulting_empfaenger = EEmpfaenger("ID", "TEXT")
        assert resulting_empfaenger.xml_attr_id == "ID"
        assert resulting_empfaenger.xml_text == "TEXT"
        assert len(vars(resulting_empfaenger)) == 2


class TestENutzdatenHeader:
    def test_attributes_set_correctly(self):
        resulting_nutzdaten_header = ENutzdatenHeader("ID", "TEXT", "VERSION", "TICKET")
        assert resulting_nutzdaten_header.Empfaenger == EEmpfaenger("ID", "TEXT")
        assert resulting_nutzdaten_header.xml_attr_version == "VERSION"
        assert resulting_nutzdaten_header.NutzdatenTicket == "TICKET"
        assert len(vars(resulting_nutzdaten_header)) == 3


class TestENutzdatenblock:
    def test_attributes_set_correctly(self, nutzdaten, default_basic_xml_construction_args):
        resulting_nutzdaten_block = ENutzdatenblock(*default_basic_xml_construction_args)
        assert resulting_nutzdaten_block.NutzdatenHeader == ENutzdatenHeader("ID", "TEXT", "VERSION", "TICKET")
        assert resulting_nutzdaten_block.Nutzdaten == nutzdaten
        assert len(vars(resulting_nutzdaten_block)) == 2


class TestEDatenTeil:
    def test_attributes_set_correctly(self, default_basic_xml_construction_args):
        resulting_daten_teil = EDatenTeil(*default_basic_xml_construction_args)
        assert resulting_daten_teil.Nutzdatenblock == ENutzdatenblock(*default_basic_xml_construction_args)
        assert len(vars(resulting_daten_teil)) == 1


class TestEElster:
    def test_attributes_set_correctly(self, default_basic_xml_construction_args):
        resulting_elster_object = EElster(*default_basic_xml_construction_args)
        assert resulting_elster_object.DatenTeil == EDatenTeil(*default_basic_xml_construction_args)
        assert resulting_elster_object.xml_attr_xmlns == "http://www.elster.de/elsterxml/schema/v11"
        assert len(vars(resulting_elster_object)) == 2


class TestEXml:
    def test_attributes_set_correctly(self, default_basic_xml_construction_args):
        resulting_xml_object = EXml(*default_basic_xml_construction_args)
        assert resulting_xml_object.Elster == EElster(*default_basic_xml_construction_args)
        assert len(vars(resulting_xml_object)) == 1


class TestConstructBasicXmlDataRepresentation:

    def test_returns_correct_object(self, default_basic_xml_construction_args):
        resulting_object = construct_basic_xml_data_representation(*default_basic_xml_construction_args)
        assert resulting_object == EXml(*default_basic_xml_construction_args)

    def test_sets_default_nutzdaten_ticket_correctly(self, nutzdaten):
        resulting_object = construct_basic_xml_data_representation("ID", "TEXT", nutzdaten, "VERSION")
        assert resulting_object == EXml("ID", "TEXT", nutzdaten, "VERSION", "1")

    def test_returns_an_object_convertable_to_valid_xml(self, default_basic_xml_construction_args):
        resulting_object = construct_basic_xml_data_representation(*default_basic_xml_construction_args)
        resulting_xml = convert_object_to_xml(resulting_object)
        ElementTree.fromstring(resulting_xml)
