from xml.etree import ElementTree

import pytest

from erica.elster_xml.common.basic_xml_data_representation import EXml
from erica.elster_xml.common.xml_conversion import convert_object_to_xml
from erica.elster_xml.grundsteuer.elster_data_representation import EAnteil, EGesetzlicherVertreter, \
    EPersonData, EGW1, ERueckuebermittlung, EVorsatz, EGrundsteuerSpecifics, EGrundsteuerData, \
    get_full_grundsteuer_data_representation, \
    EEigentumsverh, EAngFeststellung, EEmpfangsbevollmaechtigter, EWohnUnter60, EWohn60bis100, EWohnAb100, \
    EAngDurchschn, EWeitereWohn, EGaragen, EAngWohn
from erica.elster_xml.common.elsterify_fields import elsterify_anrede, elsterify_date
from erica.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import Vertreter, Anteil, Person, \
    Empfangsbevollmaechtigter, Eigentuemer
from erica.request_processing.erica_input.v2.grundsteuer_input_gebaeude import WeitereWohnraeumeDetails, GaragenAnzahl
from tests.samples.grundsteuer_sample_data import get_sample_vertreter_dict, get_sample_single_person_dict, \
    get_grundsteuer_sample_data, get_sample_empfangsbevollmaechtigter_dict, SampleGebaeude


class TestEWohnUnter60:
    def test_flaeche_under_60_should_set_fields(self):
        flaechen = [59]

        result = EWohnUnter60(flaechen)

        assert result.E7403131 == 1
        assert result.E7403132 == 59

    def test_flaeche_60_should_retain_zeroes(self):
        flaechen = [60]

        result = EWohnUnter60(flaechen)

        assert result.E7403131 == 0
        assert result.E7403132 == 0

    def test_flaechen_under_60_should_set_fields(self):
        flaechen = [59, 1]

        result = EWohnUnter60(flaechen)

        assert result.E7403131 == 2
        assert result.E7403132 == 60

    def test_flaechen_one_under_60_should_set_fields(self):
        flaechen = [59, 60]

        result = EWohnUnter60(flaechen)

        assert result.E7403131 == 1
        assert result.E7403132 == 59


class TestEWohn60bis100:
    def test_flaeche_60_should_set_fields(self):
        flaechen = [60]

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 1
        assert result.E7403142 == 60

    def test_flaeche_99_should_set_fields(self):
        flaechen = [99]

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 1
        assert result.E7403142 == 99

    def test_flaeche_100_should_retain_zeroes(self):
        flaechen = [100]

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 0
        assert result.E7403142 == 0

    def test_flaechen_under_100_should_set_fields(self):
        flaechen = [99, 60]

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 2
        assert result.E7403142 == 159

    def test_flaechen_one_under_100_should_set_fields(self):
        flaechen = [99, 100]

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 1
        assert result.E7403142 == 99


class TestEWohnAb100:
    def test_flaeche_100_should_set_fields(self):
        flaechen = [100]

        result = EWohnAb100(flaechen)

        assert result.E7403151 == 1
        assert result.E7403152 == 100

    def test_flaeche_99_should_retain_zeroes(self):
        flaechen = [99]

        result = EWohnAb100(flaechen)

        assert result.E7403151 == 0
        assert result.E7403152 == 0

    def test_flaechen_from_100_should_set_fields(self):
        flaechen = [100, 100]

        result = EWohnAb100(flaechen)

        assert result.E7403151 == 2
        assert result.E7403152 == 200

    def test_flaechen_one_under_100_should_set_fields(self):
        flaechen = [99, 100]

        result = EWohnAb100(flaechen)

        assert result.E7403151 == 1
        assert result.E7403152 == 100


class TestEWeitereWohn:
    def test_should_construct_from_dict_correctly(self):
        weitere_wohnraeume = WeitereWohnraeumeDetails.parse_obj({"anzahl": 2, "flaeche": 42})

        result = EWeitereWohn(weitere_wohnraeume)

        assert result.E7403121 == 2
        assert result.E7403122 == 42


class TestEGaragen:
    def test_should_construct_from_dict_correctly(self):
        garagen_anzahl = GaragenAnzahl.parse_obj({"anzahl_garagen": 2})

        result = EGaragen(garagen_anzahl)

        assert result.E7403171 == 2


class TestEAngDurchschn:
    def test_wohnflaeche_under_60_should_set_others_to_none(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(59).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Wohn_Unter60 is not None
        assert result.Wohn_60bis100 is None
        assert result.Wohn_ab100 is None

    def test_wohnflaeche_between_60_100_should_set_others_to_none(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(99).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Wohn_Unter60 is None
        assert result.Wohn_60bis100 is not None
        assert result.Wohn_ab100 is None

    def test_wohnflaeche_from_100_should_set_others_to_none(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(100).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Wohn_Unter60 is None
        assert result.Wohn_60bis100 is None
        assert result.Wohn_ab100 is not None

    def test_on_weitere_wohnraeume_flag_true_should_set_weitere_wohnraeume(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(10).with_weitere_wohnraeume(42, 2).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Weitere_Wohn is not None

    def test_on_weitere_wohnraeume_flag_false_should_not_set_weitere_wohnraeume(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(10).with_weitere_wohnraeume(42, 2).parse()
        gebaeude.weitere_wohnraeume.has_weitere_wohnraeume = False

        result = EAngDurchschn(gebaeude)

        assert result.Weitere_Wohn is None


class TestEAngWohn:
    def test_on_ab_1949_should_contain_baujahr(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_baujahr("1959").parse()

        result = EAngWohn(gebaeude)

        assert result.E7403114 == "1959"

    def test_on_vor_1949_should_not_contain_baujahr(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_baujahr("1959").parse()
        gebaeude.ab1949.is_ab1949 = False

        result = EAngWohn(gebaeude)

        assert result.E7403114 is None

    def test_on_kenrsaniert_should_contain_kernsanierungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_kernsanierung("1959").parse()

        result = EAngWohn(gebaeude)

        assert result.E7403115 == "1959"

    def test_on_not_kenrsaniert_should_not_contain_kernsanierungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_kernsanierung("1959").parse()
        gebaeude.kernsaniert.is_kernsaniert = False

        result = EAngWohn(gebaeude)

        assert result.E7403115 is None

    def test_on_abbruchverpflichtung_should_contain_abbruchverpflichtungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_abbruchverpflichtung("1959").parse()

        result = EAngWohn(gebaeude)

        assert result.E7403116 == "1959"

    def test_on_no_abbruchverpflichtung_should_not_contain_abbruchverpflichtungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_abbruchverpflichtung("1959").parse()
        gebaeude.abbruchverpflichtung.has_abbruchverpflichtung = False

        result = EAngWohn(gebaeude)

        assert result.E7403116 is None

    def test_on_garagen_should_contain_set_anzahl(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_garagen(2).parse()

        result = EAngWohn(gebaeude)

        assert result.Garagen.E7403171 == 2

    def test_on_no_garagen_should_contain_not_contain_garagen(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_garagen(2).parse()
        gebaeude.garagen.has_garagen = False

        result = EAngWohn(gebaeude)

        assert result.Garagen is None

    def test_should_set_ang_durchschn(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).parse()

        result = EAngWohn(gebaeude)

        assert result.Ang_Durchschn is not None


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
        assert len(vars(result)) == 11

    def test_if_part_of_optional_attributes_not_given_then_attributes_set_correctly(self):
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
        assert len(vars(result)) == 11


class TestEPersonData:
    def test_attributes_set_correctly(self):
        person_obj = Person.parse_obj(get_sample_single_person_dict())
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
        person_obj = Person.parse_obj(get_sample_single_person_dict(complete=False, with_vertreter=False))
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
        assert len(vars(result)) == 16

    def test_if_part_of_optional_attributes_not_given_then_attributes_set_correctly(self):
        person_obj = Person.parse_obj(get_sample_single_person_dict())
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
        person = get_sample_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj({"person": [person]})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "0"

    def test_if_two_married_persons_then_attributes_set_correctly(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person1, person2], "verheiratet": {"are_verheiratet": True}})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "4"

    def test_if_two_not_married_persons_then_attributes_set_correctly(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person1, person2], "verheiratet": {"are_verheiratet": False}})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "6"

    def test_if_three_persons_then_attributes_set_correctly(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        person3 = get_sample_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj({"person": [person1, person2, person3]})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "6"


class TestEAngFeststellung:
    def test_sets_attributes_correctly(self):
        result = EAngFeststellung()

        assert result.E7401311 == "1"
        assert len(vars(result)) == 1


class TestEEmpfangsbevollmaechtigter:
    def test_attributes_set_correctly(self):
        input_data = Empfangsbevollmaechtigter.parse_obj(get_sample_empfangsbevollmaechtigter_dict())

        result = EEmpfangsbevollmaechtigter(input_data)

        assert result.E7404610 == elsterify_anrede(input_data.name.anrede)
        assert result.E7404614 == input_data.name.titel
        assert result.E7404613 == input_data.name.vorname
        assert result.E7404611 == input_data.name.name
        assert result.E7404624 == input_data.adresse.strasse
        assert result.E7404625 == input_data.adresse.hausnummer
        assert result.E7404626 == input_data.adresse.hausnummerzusatz
        assert result.E7404640 == input_data.adresse.plz
        assert result.E7404627 == input_data.adresse.postfach
        assert result.E7404622 == input_data.adresse.ort
        assert result.E7412201 == input_data.telefonnummer.telefonnummer
        assert len(vars(result)) == 11

    def test_if_all_optional_attributes_not_given_then_attributes_set_correctly(self):
        input_data = Empfangsbevollmaechtigter.parse_obj(get_sample_empfangsbevollmaechtigter_dict(complete=False))

        result = EEmpfangsbevollmaechtigter(input_data)

        assert result.E7404610 == elsterify_anrede(input_data.name.anrede)
        assert result.E7404614 is None
        assert result.E7404613 == input_data.name.vorname
        assert result.E7404611 == input_data.name.name
        assert result.E7404624 is None
        assert result.E7404625 is None
        assert result.E7404626 is None
        assert result.E7404640 == input_data.adresse.plz
        assert result.E7404627 is None
        assert result.E7404622 == input_data.adresse.ort
        assert result.E7412201 is None
        assert len(vars(result)) == 11

    def test_if_part_of_optional_attributes_not_given_then_attributes_set_correctly(self):
        input_data = Empfangsbevollmaechtigter.parse_obj(get_sample_empfangsbevollmaechtigter_dict())
        input_data.name.titel = None

        result = EEmpfangsbevollmaechtigter(input_data)

        assert result.E7404610 == elsterify_anrede(input_data.name.anrede)
        assert result.E7404614 is None
        assert result.E7404613 == input_data.name.vorname
        assert result.E7404611 == input_data.name.name
        assert result.E7404624 == input_data.adresse.strasse
        assert result.E7404625 == input_data.adresse.hausnummer
        assert result.E7404626 == input_data.adresse.hausnummerzusatz
        assert result.E7404640 == input_data.adresse.plz
        assert result.E7404627 == input_data.adresse.postfach
        assert result.E7404622 == input_data.adresse.ort
        assert result.E7412201 == input_data.telefonnummer.telefonnummer
        assert len(vars(result)) == 11


class TestEGW1:

    def test_if_one_person_then_attributes_set_correctly(self):
        person = get_sample_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person], "empfangsbevollmaechtigter": get_sample_empfangsbevollmaechtigter_dict()})

        result = EGW1(eigentuemer_obj)

        assert result.Ang_Feststellung == EAngFeststellung()
        assert len(result.Eigentuemer) == 1
        assert result.Eigentuemer[0] == EPersonData(Person.parse_obj(person), person_index=0)
        assert result.Eigentumsverh == EEigentumsverh(eigentuemer_obj)
        assert result.Empfangsv == EEmpfangsbevollmaechtigter(eigentuemer_obj.empfangsbevollmaechtigter)
        assert len(vars(result)) == 4

    def test_if_no_empfangsbevollmaechtigter_set_then_attributes_set_correctly(self):
        person = get_sample_single_person_dict()
        eigentuemer_obj = Eigentuemer.parse_obj({"person": [person]})

        result = EGW1(eigentuemer_obj)

        assert result.Ang_Feststellung == EAngFeststellung()
        assert len(result.Eigentuemer) == 1
        assert result.Eigentuemer[0] == EPersonData(Person.parse_obj(person), person_index=0)
        assert result.Eigentumsverh == EEigentumsverh(eigentuemer_obj)
        assert result.Empfangsv is None
        assert len(vars(result)) == 4

    def test_if_two_persons_then_attributes_set_correctly(self):
        person1 = get_sample_single_person_dict()
        person1["persoenlicheAngaben"]["vorname"] = "Albus"
        person2 = get_sample_single_person_dict()
        person2["persoenlicheAngaben"]["vorname"] = "Rubeus"
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person1, person2], "verheiratet": {"are_verheiratet": False}})

        result = EGW1(eigentuemer_obj)

        assert result.Ang_Feststellung == EAngFeststellung()
        assert len(result.Eigentuemer) == 2
        assert result.Eigentuemer[0] == EPersonData(Person.parse_obj(person1), person_index=0)
        assert result.Eigentuemer[1] == EPersonData(Person.parse_obj(person2), person_index=1)
        assert result.Eigentumsverh == EEigentumsverh(eigentuemer_obj)
        assert result.Empfangsv is None
        assert len(vars(result)) == 4


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
