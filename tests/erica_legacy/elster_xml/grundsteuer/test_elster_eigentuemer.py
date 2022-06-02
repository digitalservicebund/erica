from unittest.mock import patch, MagicMock

from erica.erica_legacy.elster_xml.common.elsterify_fields import elsterify_anrede, elsterify_date
from erica.erica_legacy.elster_xml.grundsteuer.elster_eigentuemer import EAnteil, EGesetzlicherVertreter, EPersonData, \
    EEigentumsverh, EEmpfangsbevollmaechtigter
from erica.application.grundsteuer.grundsteuer_input_eigentuemer import Anteil, Eigentuemer
from tests.erica_legacy.samples.grundsteuer_sample_data import SampleVertreter, SampleBevollmaechtigter, SamplePerson, \
    SampleEigentuemer, DefaultSampleEigentuemer


class TestEAnteil:
    def test_attributes_set_correctly(self):
        anteil_obj = Anteil.parse_obj({'zaehler': '1', 'nenner': '2'})

        result = EAnteil(anteil_obj)

        assert result.E7404570 == anteil_obj.zaehler
        assert result.E7404571 == anteil_obj.nenner


class TestEGesetzlicherVertreter:
    def test_attributes_set_correctly(self):
        full_vertreter_obj = SampleVertreter().complete().parse()

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
        assert result.E7415604 == full_vertreter_obj.telefonnummer
        assert len(vars(result)) == 11

    def test_if_all_optional_attributes_not_given_then_attributes_set_correctly(self):
        vertreter_obj = SampleVertreter().parse()

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


class TestEPersonData:
    def test_attributes_set_correctly(self):
        person_obj = SamplePerson().with_telefonnummer().with_vertreter().parse()
        person_index = 2

        result = EPersonData(person_obj, person_index)

        assert result.Beteiligter == person_index + 1
        assert result.E7404510 == elsterify_anrede(person_obj.persoenliche_angaben.anrede)
        assert result.E7404514 == person_obj.persoenliche_angaben.titel
        assert result.E7404518 == elsterify_date(person_obj.persoenliche_angaben.geburtsdatum)
        assert result.E7404513 == person_obj.persoenliche_angaben.vorname
        assert result.E7404511 == person_obj.persoenliche_angaben.name
        assert result.E7404524 == person_obj.adresse.strasse
        assert result.E7404525 == person_obj.adresse.hausnummer
        assert result.E7404526 == person_obj.adresse.hausnummerzusatz
        assert result.E7404540 == person_obj.adresse.plz
        assert result.E7404527 == person_obj.adresse.postfach
        assert result.E7404522 == person_obj.adresse.ort
        assert result.E7414601 == person_obj.telefonnummer
        assert result.E7404519 == person_obj.steuer_id
        assert result.Anteil == EAnteil(person_obj.anteil)
        assert result.Ges_Vertreter == EGesetzlicherVertreter(person_obj.vertreter)
        assert len(vars(result)) == 16

    def test_if_all_optional_attributes_not_given_then_attributes_set_correctly(self):
        person_obj = SamplePerson().parse()
        person_index = 2

        result = EPersonData(person_obj, person_index)

        assert result.Beteiligter == person_index + 1
        assert result.E7404510 == elsterify_anrede(person_obj.persoenliche_angaben.anrede)
        assert result.E7404514 is None
        assert result.E7404518 is None
        assert result.E7404513 == person_obj.persoenliche_angaben.vorname
        assert result.E7404511 == person_obj.persoenliche_angaben.name
        assert result.E7404524 is None
        assert result.E7404525 is None
        assert result.E7404526 is None
        assert result.E7404540 == person_obj.adresse.plz
        assert result.E7404527 is None
        assert result.E7404522 == person_obj.adresse.ort
        assert result.E7414601 is None
        assert result.E7404519 == person_obj.steuer_id
        assert result.Anteil == EAnteil(person_obj.anteil)
        assert result.Ges_Vertreter is None
        assert len(vars(result)) == 16

    def test_if_part_of_optional_attributes_not_given_then_attributes_set_correctly(self):
        person_obj = SamplePerson().with_vertreter().with_telefonnummer().parse()
        person_obj.persoenliche_angaben.titel = None
        person_index = 2

        result = EPersonData(person_obj, person_index)

        assert result.Beteiligter == person_index + 1
        assert result.E7404510 == elsterify_anrede(person_obj.persoenliche_angaben.anrede)
        assert result.E7404514 is None
        assert result.E7404518 == elsterify_date(person_obj.persoenliche_angaben.geburtsdatum)
        assert result.E7404513 == person_obj.persoenliche_angaben.vorname
        assert result.E7404511 == person_obj.persoenliche_angaben.name
        assert result.E7404524 == person_obj.adresse.strasse
        assert result.E7404525 == person_obj.adresse.hausnummer
        assert result.E7404526 == person_obj.adresse.hausnummerzusatz
        assert result.E7404540 == person_obj.adresse.plz
        assert result.E7404527 == person_obj.adresse.postfach
        assert result.E7404522 == person_obj.adresse.ort
        assert result.E7414601 == person_obj.telefonnummer
        assert result.E7404519 == person_obj.steuer_id
        assert result.Anteil == EAnteil(person_obj.anteil)
        assert result.Ges_Vertreter == EGesetzlicherVertreter(person_obj.vertreter)
        assert len(vars(result)) == 16


class TestEEigentumsverh:
    def test_if_one_person_then_attributes_set_correctly(self):
        person = SamplePerson().parse()
        eigentuemer_obj = Eigentuemer.parse_obj({"person": [person]})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "0"

    def test_if_two_married_persons_then_attributes_set_correctly(self):
        person1 = SamplePerson().parse()
        person2 = SamplePerson().parse()
        eigentuemer_obj = Eigentuemer.parse_obj(
            {"person": [person1, person2], "verheiratet": True})

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "4"

    def test_if_two_not_married_persons_then_attributes_set_correctly(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        eigentuemer_obj = SampleEigentuemer().person(person1).person(person2).verheiratet(False).parse()

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "6"

    def test_if_three_persons_then_attributes_set_correctly(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        person3 = SamplePerson().build()
        eigentuemer_obj = SampleEigentuemer().person(person1).person(person2).person(person3).parse()

        result = EEigentumsverh(eigentuemer_obj)

        assert result.E7401340 == "6"


class TestEEmpfangsbevollmaechtigter:
    def test_attributes_set_correctly(self):
        eigentuemer_obj = DefaultSampleEigentuemer().empfangsbevollmaechtigter(
            SampleBevollmaechtigter().complete().build()).parse()
        
        result = EEmpfangsbevollmaechtigter(eigentuemer_obj)

        assert result.E7404610 == elsterify_anrede(eigentuemer_obj.empfangsbevollmaechtigter.name.anrede)
        assert result.E7404614 == eigentuemer_obj.empfangsbevollmaechtigter.name.titel
        assert result.E7404613 == eigentuemer_obj.empfangsbevollmaechtigter.name.vorname
        assert result.E7404611 == eigentuemer_obj.empfangsbevollmaechtigter.name.name
        assert result.E7404624 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.strasse
        assert result.E7404625 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.hausnummer
        assert result.E7404626 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.hausnummerzusatz
        assert result.E7404640 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.plz
        assert result.E7404627 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.postfach
        assert result.E7404622 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.ort
        assert result.E7412201 == eigentuemer_obj.empfangsbevollmaechtigter.telefonnummer
        assert result.E7412901 is None
        assert len(vars(result)) == 12

    def test_if_all_optional_attributes_not_given_then_attributes_set_correctly(self):
        eigentuemer_obj = DefaultSampleEigentuemer().empfangsbevollmaechtigter(
            SampleBevollmaechtigter().build()).parse()

        result = EEmpfangsbevollmaechtigter(eigentuemer_obj)

        assert result.E7404610 == elsterify_anrede(eigentuemer_obj.empfangsbevollmaechtigter.name.anrede)
        assert result.E7404614 is None
        assert result.E7404613 == eigentuemer_obj.empfangsbevollmaechtigter.name.vorname
        assert result.E7404611 == eigentuemer_obj.empfangsbevollmaechtigter.name.name
        assert result.E7404624 is None
        assert result.E7404625 is None
        assert result.E7404626 is None
        assert result.E7404640 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.plz
        assert result.E7404627 is None
        assert result.E7404622 == eigentuemer_obj.empfangsbevollmaechtigter.adresse.ort
        assert result.E7412201 is None
        assert result.E7412901 is None
        assert len(vars(result)) == 12

    def test_if_no_bruchteilsgemeinschaft_set_flag_to_none(self):
        eigentuemer_obj = DefaultSampleEigentuemer().empfangsbevollmaechtigter(
            SampleBevollmaechtigter().complete().build()).parse()

        with patch('erica.erica_legacy.elster_xml.common.elsterify_fields.elsterify_eigentumsverhaeltnis',
                   MagicMock(return_value="1")):
            result = EEmpfangsbevollmaechtigter(eigentuemer_obj)

        assert result.E7412901 is None

    def test_if_bruchteilsgemeinschaft_set_flag_to_1(self):
        eigentuemer_obj = DefaultSampleEigentuemer().empfangsbevollmaechtigter(
            SampleBevollmaechtigter().complete().build()).parse()

        with patch('erica.erica_legacy.elster_xml.grundsteuer.elster_eigentuemer.elsterify_eigentumsverhaeltnis',
                   MagicMock(return_value="6")):
            result = EEmpfangsbevollmaechtigter(eigentuemer_obj)

        assert result.E7412901 == 1
