import pytest
from pydantic import ValidationError

from erica.application.grundsteuer.grundsteuer_input_grundstueck  import Flurstueck, Grundstueck, \
    Grundstuecksart
from tests.erica_legacy.samples.grundsteuer_sample_data import SampleFlurstueck, SampleGrundstueck


class TestGrundstuecksart:
    def test_einfamilienhaus(self):
        assert Grundstuecksart.einfamilienhaus.is_bebaut() is True

    def test_zweifamilienhaus(self):
        assert Grundstuecksart.zweifamilienhaus.is_bebaut() is True

    def test_wohnungseigentum(self):
        assert Grundstuecksart.wohnungseigentum.is_bebaut() is True

    def test_baureif(self):
        assert Grundstuecksart.baureif.is_bebaut() is False

    def test_abweichende_entwicklung(self):
        assert Grundstuecksart("abweichendeEntwicklung") == Grundstuecksart.abweichende_entwicklung
        assert Grundstuecksart.abweichende_entwicklung.is_bebaut() is False


class TestFlur:
    def test_if_w_einheit_zaehler_5_decimal_places_then_raise_error(self):
        input_data = SampleFlurstueck().w_einheit_zaehler("1.00000").w_einheit_nenner(10).build()

        with pytest.raises(ValidationError):
            Flurstueck.parse_obj(input_data)

    def test_if_w_einheit_zaehler_contains_nondigits_then_raise_error(self):
        input_data = SampleFlurstueck().w_einheit_zaehler("1.0a00").w_einheit_nenner(10).build()

        with pytest.raises(ValidationError):
            Flurstueck.parse_obj(input_data)

    def test_if_w_einheit_zaehler_7_int_digits_then_raise_error(self):
        input_data = SampleFlurstueck().w_einheit_zaehler("1234567.0000").w_einheit_nenner(10).build()

        with pytest.raises(ValidationError):
            Flurstueck.parse_obj(input_data)

    def test_if_w_einheit_zaehler_6_int_digits_then_parse_correctly(self):
        input_data = SampleFlurstueck().w_einheit_zaehler("123456.0000").w_einheit_nenner(10).build()

        result = Flurstueck.parse_obj(input_data)

        assert result.flur.wirtschaftliche_einheit_zaehler == "123456.0000"

    def test_if_w_einheit_zaehler_given_nenner_missing_then_raise_error(self):
        input_data = SampleFlurstueck().w_einheit_zaehler("1.0000").build()

        with pytest.raises(ValidationError):
            Flurstueck.parse_obj(input_data)

    def test_if_w_einheit_nenner_given_zaehler_missing_then_raise_error(self):
        input_data = SampleFlurstueck().w_einheit_nenner(1).build()

        with pytest.raises(ValidationError):
            Flurstueck.parse_obj(input_data)

    def test_if_neither_w_einheit_zaehler_nor_nenner_given_then_should_set_default_values(self):
        input_data = SampleFlurstueck().build()

        result = Flurstueck.parse_obj(input_data).flur

        assert result.wirtschaftliche_einheit_zaehler == "1.0000"
        assert result.wirtschaftliche_einheit_nenner == 1

    def test_if_both_w_einheit_zaehler_nenner_given_then_should_parse_values(self):
        input_data = SampleFlurstueck().w_einheit_zaehler("1.4200").w_einheit_nenner(42).build()

        result = Flurstueck.parse_obj(input_data).flur

        assert result.wirtschaftliche_einheit_zaehler == "1.4200"
        assert result.wirtschaftliche_einheit_nenner == 42


class TestGrundstueck:
    def test_if_bebaut_and_strasse_not_set_then_raise_error(self):
        grundstueck = SampleGrundstueck().strasse(None).hausnummer(None).build()

        with pytest.raises(ValidationError):
            Grundstueck.parse_obj(grundstueck)

    def test_if_bebaut_and_plz_not_set_then_raise_error(self):
        grundstueck = SampleGrundstueck().strasse("foo").plz(None).ort("bar").build()

        with pytest.raises(ValidationError):
            Grundstueck.parse_obj(grundstueck)

    def test_if_bebaut_and_ort_not_set_then_raise_error(self):
        grundstueck = SampleGrundstueck().strasse("foo").plz("12345").ort(None).build()

        with pytest.raises(ValidationError):
            Grundstueck.parse_obj(grundstueck)

    def test_if_bebaut_and_strasse_plz_ort_set_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().strasse("foo").plz("12345").ort("bar").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.adresse.strasse == "foo"
        assert result.adresse.plz == "12345"
        assert result.adresse.ort == "bar"

    def test_if_typ_einfamilienhaus_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().typ("einfamilienhaus").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.typ == "einfamilienhaus"

    def test_if_typ_zweifamilienhaus_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().typ("zweifamilienhaus").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.typ == "zweifamilienhaus"

    def test_if_typ_wohnungseigentum_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().typ("wohnungseigentum").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.typ == "wohnungseigentum"

    def test_if_typ_baureif_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().typ("baureif").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.typ == "baureif"

    def test_if_typ_abweichende_entwicklung_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().typ("abweichendeEntwicklung").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.typ == "abweichendeEntwicklung"

    def test_if_typ_invalid_then_should_raise_error(self):
        grundstueck = SampleGrundstueck().typ("invalid").build()

        with pytest.raises(ValidationError):
            Grundstueck.parse_obj(grundstueck)

    def test_if_abweichende_entwicklung_bauerwartungsland_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().abweichende_enwticklung("bauerwartungsland").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.abweichende_entwicklung == "bauerwartungsland"

    def test_if_abweichende_entwicklung_rohbauland_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().abweichende_enwticklung("rohbauland").build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.abweichende_entwicklung == "rohbauland"

    def test_if_abweichende_entwicklung_none_then_should_parse_correctly(self):
        grundstueck = SampleGrundstueck().abweichende_enwticklung(None).build()

        result = Grundstueck.parse_obj(grundstueck)

        assert result.abweichende_entwicklung is None

    def test_if_abweichende_entwicklung_invalid_then_should_raise_error(self):
        grundstueck = SampleGrundstueck().abweichende_enwticklung("invalid").build()

        with pytest.raises(ValidationError):
            Grundstueck.parse_obj(grundstueck)
