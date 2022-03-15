import pytest
from pydantic import ValidationError

from erica.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import SteuerId, Verheiratet, Person, \
    Eigentuemer
from erica.request_processing.erica_input.v2.grundsteuer_input_gebaeude import Ab1949, Kernsaniert, \
    Abbruchverpflichtung, WeitereWohnraeume, WeitereWohnraeumeDetails, Garagen, GaragenAnzahl, Gebaeude
from tests.samples.grundsteuer_sample_data import get_sample_single_person_dict, SampleGebaeude


class TestAb1949:
    def test_on_camel_case_should_map_to_snake_case(self):
        input_data = {"isAb1949": True}

        result = Ab1949.parse_obj(input_data)

        assert result.is_ab1949 is True

    def test_foo(self):
        gebaeude = SampleGebaeude().with_baujahr("1950").build()
        print(gebaeude)


class TestAbbruchverpflichtung:
    def test_on_camel_case_should_map_to_snake_case(self):
        input_data = {"hasAbbruchverpflichtung": True}

        result = Abbruchverpflichtung.parse_obj(input_data)

        assert result.has_abbruchverpflichtung is True


class TestGaragen:
    def test_on_camel_case_should_map_to_snake_case(self):
        input_data = {"hasGaragen": True}

        result = Garagen.parse_obj(input_data)

        assert result.has_garagen is True


class TestGaragenAnzahl:
    def test_on_camel_case_should_map_to_snake_case(self):
        input_data = {"anzahlGaragen": 3}

        result = GaragenAnzahl.parse_obj(input_data)

        assert result.anzahl_garagen == 3


class TestKernsaniert:
    def test_on_camel_case_should_map_to_snake_case(self):
        input_data = {"isKernsaniert": True}

        result = Kernsaniert.parse_obj(input_data)

        assert result.is_kernsaniert is True


class TestWeitereWohnraeume:
    def test_on_camel_case_should_map_to_snake_case(self):
        input_data = {"has_weitere_wohnraeume": True}

        result = WeitereWohnraeume.parse_obj(input_data)

        assert result.has_weitere_wohnraeume is True


class TestWeitereWohnraeumeFlaeche:
    def test_on_camel_case_should_map_to_snake_case(self):
        input_data = {"anzahl": "2", "flaeche": "42"}

        result = WeitereWohnraeumeDetails.parse_obj(input_data)

        assert result.anzahl == 2
        assert result.flaeche == 42


class TestGebaeude:
    def test_on_is_ab1949_but_no_baujahr_should_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaeche("42").with_baujahr().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_on_is_ab1949_and_baujahr_should_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_baujahr("1970").build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.baujahr.baujahr == "1970"

    def test_on_is_kernsaniert_but_no_kernsanierungsjahr_should_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_kernsanierung().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_on_is_kernsaniert_and_kernsanierungsjahr_should_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_kernsanierung("1970").build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.kernsanierungsjahr.kernsanierungsjahr == "1970"

    def test_on_has_abbruchverpflichtung_but_no_jahr_should_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_abbruchverpflichtung().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_on_has_abbruchverpflichtung_and_jahr_should_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_abbruchverpflichtung("1970").build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.abbruchverpflichtungsjahr.abbruchverpflichtungsjahr == "1970"

    def test_on_neither_wohnflaeche_nor_wohnflaechen_should_raise_error(self):
        gebaeude = SampleGebaeude().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_on_both_wohnflaeche_and_wohnflaechen_should_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(1).with_wohnflaechen(2, 3).build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_on_only_wohnflaeche_should_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(1).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.wohnflaeche.wohnflaeche == 1

    def test_on_only_wohnflaechen_should_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(2, 3).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.wohnflaechen.wohnflaeche1 == 2
        assert result.wohnflaechen.wohnflaeche2 == 3

    def test_on_has_weitere_wohnraeume_but_no_ww_flaeche_should_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_weitere_wohnraeume().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_on_has_weitere_wohnraeume_and_ww_flaeche_should_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_weitere_wohnraeume(24, 2).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.weitere_wohnraeume_details.anzahl == 2
        assert result.weitere_wohnraeume_details.flaeche == 24

    def test_on_has_garagen_but_no_anzahl_should_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaeche("42").with_garagen().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_on_has_garagen_and_anzahl_should_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaeche(42).with_garagen(2).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.garagen_anzahl.anzahl_garagen == 2


class TestVerheiratet:
    def test_if_snake_case_given_then_include_in_resulting_object(self):
        input_data = {"are_verheiratet": True}

        result = Verheiratet.parse_obj(input_data)

        assert result.are_verheiratet is True

    def test_if_camel_case_given_then_include_in_resulting_object(self):
        input_data = {"areVerheiratet": True}

        result = Verheiratet.parse_obj(input_data)

        assert result.are_verheiratet is True


class TestSteuerId:
    def test_if_snake_case_given_then_include_in_resulting_object(self):
        input_data = {"steuer_id": "ID"}

        result = SteuerId.parse_obj(input_data)

        assert result.steuer_id == input_data["steuer_id"]

    def test_if_camel_case_given_then_include_in_resulting_object(self):
        input_data = {"steuerId": "ID"}

        result = SteuerId.parse_obj(input_data)

        assert result.steuer_id == input_data["steuerId"]


class TestPerson:
    def test_if_snake_case_given_then_include_in_resulting_object(self):
        input_data = get_sample_single_person_dict()
        input_data["steuer_id"]["steuer_id"] = "ID"

        result = Person.parse_obj(input_data)

        assert result.steuer_id.steuer_id == input_data["steuer_id"]["steuer_id"]

    def test_if_camel_case_given_then_include_in_resulting_object(self):
        input_data = get_sample_single_person_dict()
        input_data["steuerId"] = {"steuerId": "ID"}
        input_data.pop("steuer_id")

        result = Person.parse_obj(input_data)

        assert result.steuer_id.steuer_id == input_data["steuerId"]["steuerId"]

    def test_if_mixed_case_given_then_include_in_resulting_object(self):
        input_data = get_sample_single_person_dict()
        input_data["steuerId"] = {"steuer_id": "ID"}
        input_data.pop("steuer_id")

        result = Person.parse_obj(input_data)

        assert result.steuer_id.steuer_id == input_data["steuerId"]["steuer_id"]


class TestEigentuemer:
    def test_if_one_person_and_verheiratet_not_given_then_do_not_raise_error(self):
        person = get_sample_single_person_dict()
        input_data = {"person": [person]}
        Eigentuemer.parse_obj(input_data)

    def test_if_one_person_and_verheiratet_true_then_raise_error(self):
        person = get_sample_single_person_dict()
        input_data = {"person": [person], "verheiratet": {"are_verheiratet": True}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_one_person_and_verheiratet_false_then_raise_error(self):
        person = get_sample_single_person_dict()
        input_data = {"person": [person], "verheiratet": {"are_verheiratet": False}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_true_then_do_not_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {"are_verheiratet": True}}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_false_then_do_not_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {"are_verheiratet": False}}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_not_given_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2]}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_given_but_are_verheiratet_not_set_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_three_persons_and_verheiratet_true_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        person3 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2, person3], "verheiratet": {"are_verheiratet": True}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_three_persons_and_verheiratet_false_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        person3 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2, person3], "verheiratet": {"are_verheiratet": False}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)
