from xml.etree import ElementTree

import pytest

from erica.erica_legacy.elster_xml.common.basic_xml_data_representation import EXml
from erica.erica_legacy.elster_xml.common.xml_conversion import convert_object_to_xml
from erica.erica_legacy.elster_xml.grundsteuer.elster_data_representation import ERueckuebermittlung, EVorsatz, EGrundsteuerSpecifics, EGrundsteuerData, \
    get_full_grundsteuer_data_representation
from erica.erica_legacy.elster_xml.grundsteuer.elster_eigentuemer import EGW1
from tests.erica_legacy.samples.grundsteuer_sample_data import get_grundsteuer_sample_data


class TestERueckuebermittlung:
    def test_attributes_set_correctly(self):
        result = ERueckuebermittlung()

        assert result.Bescheid == "2"
        assert len(vars(result)) == 1


class TestEVorsatz:
    def test_attributes_set_correctly(self):
        grundsteuer_obj = get_grundsteuer_sample_data()

        result = EVorsatz(grundsteuer_obj)

        assert result.Unterfallart == "88"
        assert result.Vorgang == "01"
        # TODO assert result.StNr == grundsteuer_obj.grundstueck.stnr.stnr
        assert result.Zeitraum == "2022"
        assert result.AbsName == grundsteuer_obj.eigentuemer.person[0].persoenlicheAngaben.vorname + \
               " " + \
               grundsteuer_obj.eigentuemer.person[0].persoenlicheAngaben.name
        assert result.AbsStr == grundsteuer_obj.eigentuemer.person[0].adresse.strasse
        assert result.AbsPlz == grundsteuer_obj.eigentuemer.person[0].adresse.plz
        assert result.AbsOrt == grundsteuer_obj.eigentuemer.person[0].adresse.ort
        assert result.Copyright == "(C) 2022 DigitalService4Germany"
        assert result.OrdNrArt == "S"
        assert result.Rueckuebermittlung == ERueckuebermittlung()
        assert len(vars(result)) == 11


class TestEGrundsteuerSpecifics:
    def test_attributes_set_correctly(self):
        grundsteuer_obj = get_grundsteuer_sample_data()

        result = EGrundsteuerSpecifics(grundsteuer_obj)

        assert result.Vorsatz == EVorsatz(grundsteuer_obj)
        assert result.GW1 == EGW1(grundsteuer_obj.eigentuemer)
        assert result.xml_attr_version == "2"
        assert result.xml_attr_xmlns == "http://finkonsens.de/elster/elstererklaerung/grundsteuerwert/e88/v2"
        assert len(vars(result)) == 5


class TestEGrundsteuerData:
    def test_attributes_set_correctly(self):
        grundsteuer_obj = get_grundsteuer_sample_data()

        result = EGrundsteuerData(grundsteuer_obj)

        assert result.E88 == EGrundsteuerSpecifics(grundsteuer_obj)
        assert len(vars(result)) == 1


class TestGetFullGrundsteuerDataRepresentation:
    def test_returns_full_xml_including_grundsteuer_object(self):
        grundsteuer_obj = get_grundsteuer_sample_data()

        result = get_full_grundsteuer_data_representation(grundsteuer_obj)

        assert len(vars(result)) == 1
        assert isinstance(result, EXml)
        assert result.Elster.DatenTeil.Nutzdatenblock.Nutzdaten == EGrundsteuerData(grundsteuer_obj)

    def test_sets_empfaenger_data_correctly(self):
        grundsteuer_obj = get_grundsteuer_sample_data()

        result = get_full_grundsteuer_data_representation(grundsteuer_obj)
        empfaenger_result = result.Elster.DatenTeil.Nutzdatenblock.NutzdatenHeader.Empfaenger
        assert empfaenger_result.xml_attr_id == "F"
        # TODO assert empfaenger_result.xml_text == get_bufa_nr(...)

    def test_sets_nutzdaten_header_version_correctly(self):
        grundsteuer_obj = get_grundsteuer_sample_data()

        result = get_full_grundsteuer_data_representation(grundsteuer_obj)
        assert result.Elster.DatenTeil.Nutzdatenblock.NutzdatenHeader.xml_attr_version == "11"

    def test_returns_an_object_convertable_to_valid_xml(self):
        grundsteuer_obj = get_grundsteuer_sample_data()
        resulting_object = get_full_grundsteuer_data_representation(grundsteuer_obj)
        resulting_xml = convert_object_to_xml(resulting_object)
        try:
            ElementTree.fromstring(resulting_xml)
        except ElementTree.ParseError as e:
            return pytest.fail("Did not result in a valid xml: \n" + e.msg)
