import datetime

import pytest

from erica.worker.elster_xml.common.elsterify_fields import elsterify_anrede, elsterify_date, \
    elsterify_grundstuecksart, elsterify_wirtschaftliche_einheit_zaehler, elsterify_eigentumsverhaeltnis
from erica.api.dto.grundsteuer_input_eigentuemer import Anrede
from erica.api.dto.grundsteuer_input_grundstueck import Grundstuecksart
from tests.worker.samples.grundsteuer_sample_data import SampleEigentuemer, SamplePerson


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


class TestElsterifyGrundstuecksart:
    def test_baureif_is_correctly_translated(self):
        result = elsterify_grundstuecksart(Grundstuecksart.baureif)

        assert result == 1

    def test_abweichende_entwicklung_is_correctly_translated(self):
        result = elsterify_grundstuecksart(Grundstuecksart.abweichende_entwicklung)

        assert result == 1

    def test_einfamilienhaus_is_correctly_translated(self):
        result = elsterify_grundstuecksart(Grundstuecksart.einfamilienhaus)

        assert result == 2

    def test_zweifamilienhaus_is_correctly_translated(self):
        result = elsterify_grundstuecksart(Grundstuecksart.zweifamilienhaus)

        assert result == 3

    def test_wohnungseigentum_is_correctly_translated(self):
        result = elsterify_grundstuecksart(Grundstuecksart.wohnungseigentum)

        assert result == 5

    def test_invalid_value_raises_key_error(self):
        with pytest.raises(KeyError):
            elsterify_grundstuecksart("INVALID")


class TestElsterifyEigentumsverhaeltnis:
    def test_if_one_person_then_return_01(self):
        eigentuemer_obj = SampleEigentuemer().person(SamplePerson().build()).parse()

        result = elsterify_eigentumsverhaeltnis(eigentuemer_obj)

        assert result == "0"

    def test_if_two_married_persons_then_attributes_set_correctly(self):
        person1 = SamplePerson().parse()
        person2 = SamplePerson().parse()
        eigentuemer_obj = SampleEigentuemer().person(person1).person(person2).verheiratet(True).parse()

        result = elsterify_eigentumsverhaeltnis(eigentuemer_obj)

        assert result == "4"

    def test_if_two_not_married_persons_then_attributes_set_correctly(self):
        person1 = SamplePerson().parse()
        person2 = SamplePerson().parse()
        eigentuemer_obj = SampleEigentuemer().person(person1).person(person2).verheiratet(False).parse()

        result = elsterify_eigentumsverhaeltnis(eigentuemer_obj)

        assert result == "6"

    def test_if_three_persons_then_attributes_set_correctly(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        person3 = SamplePerson().build()
        eigentuemer_obj = SampleEigentuemer().person(person1).person(person2).person(person3).parse()

        result = elsterify_eigentumsverhaeltnis(eigentuemer_obj)

        assert result == "6"


class TestElsterifyDate:
    def test_if_valid_date_then_return_correct_format(self):
        result = elsterify_date(datetime.date(1987, 2, 1))
        assert result == "01.02.1987"

    def test_if_none_given_then_return_none(self):
        result = elsterify_date(None)
        assert result is None

    def test_if_invalid_date_then_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            elsterify_date("INVALID")


class TestElsterifyWirtschaftlicheEinheitZaehler:
    def test_if_valid_string_with_dot_then_replaces_dot_by_comma(self):
        result = elsterify_wirtschaftliche_einheit_zaehler("1.0000")
        assert result == "1,0000"

    def test_if_valid_string_without_dot_then_return_as_is(self):
        result = elsterify_wirtschaftliche_einheit_zaehler("10000")
        assert result == "10000"

    def test_if_none_then_return_none(self):
        result = elsterify_wirtschaftliche_einheit_zaehler(None)
        assert result is None

    def test_if_not_string_then_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            elsterify_wirtschaftliche_einheit_zaehler(1)
