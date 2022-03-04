import datetime
from xml.etree import ElementTree

import pytest

from erica.elster_xml.common.basic_xml_data_representation import EXml
from erica.elster_xml.common.xml_conversion import convert_object_to_xml
from erica.elster_xml.grundsteuer.elster_data_representation import elsterify_anrede, EAnteil, EGesetzlicherVertreter, \
    EPersonData, EGW1, ERueckuebermittlung, EVorsatz, EGrundsteuerSpecifics, EGrundsteuerData, get_full_grundsteuer_data_representation, \
    EEigentumsverh, EAngFeststellung, elsterify_date
from erica.request_processing.erica_input.v2.grundsteuer_input import Anrede, Anteil, Vertreter, Person, Eigentuemer
from tests.samples.grundsteuer_sample_data import get_sample_vertreter_dict, get_single_person_dict, create_grundsteuer


class TestElsterifyAnrede:
    def test_no_anrede_is_correctly_translated(self):
        result = elsterify_anrede(Anrede.no_anrede)
        assert result == '01'

    def test_herr_is_correctly_translated(self):
        result = elsterify_anrede(Anrede.herr)
        assert result == '02'

    def test_frau_is_correctly_translated(self):
        result = elsterify_anrede(Anrede.frau)
        assert result == '03'

    def test_invalid_value_raises_key_error(self):
        with pytest.raises(KeyError):
            elsterify_anrede("INVALID")


class TestElsterifyDate:
    def test_if_valid_date_then_return_correct_format(self):
        result = elsterify_date(datetime.date(1987, 2, 1))
        assert result == "01.02.1987"

    def test_if_invalid_date_then_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            elsterify_date("INVALID")


class TestEAnteil:
    def test_attributes_set_correctly(self):
        anteil_obj = Anteil.parse_obj({'zaehler': '1', 'nenner': '2'})

        result = EAnteil(anteil_obj)

        assert result.E7404570 == anteil_obj.zaehler
        assert result.E7404571 == anteil_obj.nenner


class TestEGesetzlicherVertreter:
    def test_attributes_set_correctly(self):
        full_vertreter_obj = Vertreter.parse_obj(get_sample_vertreter_dict())

        result = EGesetzlicherVertreter(full_vertreter_obj)

        assert result.E7415101 == elsterify_anrede(full_vertreter_obj.name.anrede)
        assert result.E7415102 == full_vertreter_obj.name.titel
        assert result.E7415201 == full_vertreter_obj.name.vorname
        assert result.E7415301 == full_vertreter_obj.name.name
        assert result.E7415401 == full_vertreter_obj.adresse.strasse
        assert result.E7415501 == full_vertreter_obj.adresse.hausnummer
        assert result.E7415502 == full_vertreter_obj.adresse.hausnummerzusatz
        assert result.E7415601 == full_vertreter_obj.adresse.plz
        assert result.E7415602 == full_vertreter_obj.adresse.postfach
        assert result.E7415603 == full_vertreter_obj.adresse.ort
        assert result.E7415604 == full_vertreter_obj.telefonnummer.telefonnummer
        assert len(vars(result)) == 11

    def test_if_all_optional_attributes_not_given_then_attributes_set_correctly(self):
        vertreter_obj = Vertreter.parse_obj(get_sample_vertreter_dict(complete=False))

        result = EGesetzlicherVertreter(vertreter_obj)

        assert result.E7415101 == elsterify_anrede(vertreter_obj.name.anrede)
        assert result.E7415102 is None
        assert result.E7415201 == vertreter_obj.name.vorname
        assert result.E7415301 == vertreter_obj.name.name
        assert result.E7415401 is None
        assert result.E7415501 is None
        assert result.E7415502 is None
        assert result.E7415601 == vertreter_obj.adresse.plz
        assert result.E7415602 is None
        assert result.E7415603 == vertreter_obj.adresse.ort
        assert result.E7415604 is None
        assert len(vars(result)) <= 11

    def test_if_first_part_of_optional_attributes_not_given_then_attributes_set_correctly(self):
        vertreter_obj = Vertreter.parse_obj(get_sample_vertreter_dict(complete=True))
        vertreter_obj.name.titel = None
        vertreter_obj.adresse.strasse = None

        result = EGesetzlicherVertreter(vertreter_obj)

        assert result.E7415101 == elsterify_anrede(vertreter_obj.name.anrede)
        assert result.E7415102 is None
        assert result.E7415201 == vertreter_obj.name.vorname
        assert result.E7415301 == vertreter_obj.name.name
        assert result.E7415401 is None
        assert result.E7415501 == vertreter_obj.adresse.hausnummer
        assert result.E7415502 == vertreter_obj.adresse.hausnummerzusatz
        assert result.E7415601 == vertreter_obj.adresse.plz
        assert result.E7415602 == vertreter_obj.adresse.postfach
        assert result.E7415603 == vertreter_obj.adresse.ort
        assert result.E7415604 == vertreter_obj.telefonnummer.telefonnummer
        assert len(vars(result)) <= 11


class TestEPersonData:
    def test_attributes_set_correctly(self):
        person_obj = Person.parse_obj(get_single_person_dict())
        person_index = 2

        result = EPersonData(person_obj, person_index)

        assert result.Beteiligter == person_index + 1
        assert result.E7404510 == elsterify_anrede(person_obj.persoenlicheAngaben.anrede)
        assert result.E7404514 == person_obj.persoenlicheAngaben.titel
        assert result.E7404518 == elsterify_date(person_obj.persoenlicheAngaben.geburtsdatum)
        assert result.E7404513 == person_obj.persoenlicheAngaben.vorname
        assert result.E7404511 == person_obj.persoenlicheAngaben.name
        assert result.E7404524 == person_obj.adresse.strasse
        assert result.E7404525 == person_obj.adresse.hausnummer
        assert result.E7404526 == person_obj.adresse.hausnummerzusatz
        assert result.E7404540 == person_obj.adresse.plz
        assert result.E7404527 == person_obj.adresse.postfach
        assert result.E7404522 == person_obj.adresse.ort
        assert result.E7414601 == person_obj.telefonnummer.telefonnummer
        assert result.E7404519 == person_obj.steuer_id.steuer_id
        assert result.Anteil == EAnteil(person_obj.anteil)
        assert result.Ges_Vertreter == EGesetzlicherVertreter(person_obj.vertreter)
        assert len(vars(result)) == 16

    def test_if_all_optional_attributes_not_given_then_attributes_set_correctly(self):
        person_obj = Person.parse_obj(get_single_person_dict(complete=False, with_vertreter=False))
        person_index = 2

        result = EPersonData(person_obj, person_index)

        assert result.Beteiligter == person_index + 1
        assert result.E7404510 == elsterify_anrede(person_obj.persoenlicheAngaben.anrede)
        assert result.E7404514 is None
        assert result.E7404518 is None
        assert result.E7404513 == person_obj.persoenlicheAngaben.vorname
        assert result.E7404511 == person_obj.persoenlicheAngaben.name
        assert result.E7404524 is None
        assert result.E7404525 is None
        assert result.E7404526 is None
        assert result.E7404540 == person_obj.adresse.plz
        assert result.E7404527 is None
        assert result.E7404522 == person_obj.adresse.ort
        assert result.E7414601 is None
        assert result.E7404519 == person_obj.steuer_id.steuer_id
        assert result.Anteil == EAnteil(person_obj.anteil)
        assert result.Ges_Vertreter is None
        assert len(vars(result)) <= 16

    def test_if_first_part_of_optional_attributes_not_given_then_attributes_set_correctly(self):
        person_obj = Person.parse_obj(get_single_person_dict())
        person_obj.persoenlicheAngaben.titel = None
        person_index = 2

        result = EPersonData(person_obj, person_index)

        assert result.Beteiligter == person_index + 1
        assert result.E7404510 == elsterify_anrede(person_obj.persoenlicheAngaben.anrede)
        assert result.E7404514 is None
        assert result.E7404518 == elsterify_date(person_obj.persoenlicheAngaben.geburtsdatum)
        assert result.E7404513 == person_obj.persoenlicheAngaben.vorname
        assert result.E7404511 == person_obj.persoenlicheAngaben.name
        assert result.E7404524 == person_obj.adresse.strasse
        assert result.E7404525 == person_obj.adresse.hausnummer
        assert result.E7404526 == person_obj.adresse.hausnummerzusatz
        assert result.E7404540 == person_obj.adresse.plz
        assert result.E7404527 == person_obj.adresse.postfach
        assert result.E7404522 == person_obj.adresse.ort
        assert result.E7414601 == person_obj.telefonnummer.telefonnummer
        assert result.E7404519 == person_obj.steuer_id.steuer_id
        assert result.Anteil == EAnteil(person_obj.anteil)
        assert result.Ges_Vertreter == EGesetzlicherVertreter(person_obj.vertreter)
        assert len(vars(result)) == 16


class TestEEigentumsverh:
    def test_if_one_person_then_attributes_set_correctly(self):
        person = get_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj({"person": [person]})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "0"

    def test_if_two_married_persons_then_attributes_set_correctly(self):
        person1 = get_single_person_dict()
        person2 = get_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person1, person2], "verheiratet": {"are_verheiratet": True}})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "4"

    def test_if_two_not_married_persons_then_attributes_set_correctly(self):
        person1 = get_single_person_dict()
        person2 = get_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person1, person2], "verheiratet": {"are_verheiratet": False}})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "6"

    def test_if_three_persons_then_attributes_set_correctly(self):
        person1 = get_single_person_dict()
        person2 = get_single_person_dict()
        person3 = get_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj({"person": [person1, person2, person3]})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "6"


class TestEAngFeststellung:
    def test_sets_attributes_correctly(self):
        result = EAngFeststellung()

        assert result.E7401311 == "1"
        assert len(vars(result)) == 1


class TestEGW1:
    def test_if_one_person_then_attributes_set_correctly(self):
        person = get_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj({"person": [person]})

        result = EGW1(eigentuemer_obj)

        assert result.Ang_Feststellung == EAngFeststellung()
        assert len(result.Eigentuemer) == 1
        assert result.Eigentuemer[0] == EPersonData(Person.parse_obj(person), person_index=0)
        assert result.Eigentumsverh == EEigentumsverh(eigentuemer_obj)
        assert len(vars(result)) == 3

    def test_if_two_persons_then_attributes_set_correctly(self):
        person1 = get_single_person_dict()
        person1["persoenlicheAngaben"]["vorname"] = "Albus"
        person2 = get_single_person_dict()
        person2["persoenlicheAngaben"]["vorname"] = "Rubeus"
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person1, person2], "verheiratet": {"are_verheiratet": False}})

        result = EGW1(eigentuemer_obj)

        assert result.Ang_Feststellung == EAngFeststellung()
        assert len(result.Eigentuemer) == 2
        assert result.Eigentuemer[0] == EPersonData(Person.parse_obj(person1), person_index=0)
        assert result.Eigentuemer[1] == EPersonData(Person.parse_obj(person2), person_index=1)
        assert result.Eigentumsverh == EEigentumsverh(eigentuemer_obj)
        assert len(vars(result)) == 3


class TestERueckuebermittlung:
    def test_attributes_set_correctly(self):
        result = ERueckuebermittlung()

        assert result.Bescheid == "2"
        assert len(vars(result)) == 1


class TestEVorsatz:
    def test_attributes_set_correctly(self):
        grundsteuer_obj = create_grundsteuer()

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
        grundsteuer_obj = create_grundsteuer()

        result = EGrundsteuerSpecifics(grundsteuer_obj)

        assert result.Vorsatz == EVorsatz(grundsteuer_obj)
        assert result.GW1 == EGW1(grundsteuer_obj.eigentuemer)
        assert result.xml_attr_version == "2"
        assert result.xml_attr_xmlns == "http://finkonsens.de/elster/elstererklaerung/grundsteuerwert/e88/v2"
        assert len(vars(result)) == 4


class TestEGrundsteuerData:
    def test_attributes_set_correctly(self):
        grundsteuer_obj = create_grundsteuer()

        result = EGrundsteuerData(grundsteuer_obj)

        assert result.E88 == EGrundsteuerSpecifics(grundsteuer_obj)
        assert len(vars(result)) == 1


class TestGetFullGrundsteuerDataRepresentation:
    def test_returns_full_xml_including_grundsteuer_object(self):
        grundsteuer_obj = create_grundsteuer()

        result = get_full_grundsteuer_data_representation(grundsteuer_obj)

        assert len(vars(result)) == 1
        assert isinstance(result, EXml)
        assert result.Elster.DatenTeil.Nutzdatenblock.Nutzdaten == EGrundsteuerData(grundsteuer_obj)

    def test_sets_empfaenger_data_correctly(self):
        grundsteuer_obj = create_grundsteuer()

        result = get_full_grundsteuer_data_representation(grundsteuer_obj)
        empfaenger_result = result.Elster.DatenTeil.Nutzdatenblock.NutzdatenHeader.Empfaenger
        assert empfaenger_result.xml_attr_id == "F"
        # TODO assert empfaenger_result.xml_text == get_bufa_nr(...)

    def test_sets_nutzdaten_header_version_correctly(self):
        grundsteuer_obj = create_grundsteuer()

        result = get_full_grundsteuer_data_representation(grundsteuer_obj)
        assert result.Elster.DatenTeil.Nutzdatenblock.NutzdatenHeader.xml_attr_version == "11"

    def test_returns_an_object_convertable_to_valid_xml(self):
        grundsteuer_obj = create_grundsteuer()
        resulting_object = get_full_grundsteuer_data_representation(grundsteuer_obj)
        resulting_xml = convert_object_to_xml(resulting_object)
        try:
            ElementTree.fromstring(resulting_xml)
        except ElementTree.ParseError as e:
            return pytest.fail("Did not result in a valid xml: \n" + e.msg)
