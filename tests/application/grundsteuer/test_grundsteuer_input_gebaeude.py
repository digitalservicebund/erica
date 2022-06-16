import pytest
from pydantic import ValidationError

from erica.application.grundsteuer.grundsteuer_input_gebaeude import Ab1949, \
    Abbruchverpflichtung, Garagen, GaragenAnzahl, Kernsaniert, WeitereWohnraeume, WeitereWohnraeumeDetails, Gebaeude
from tests.erica_legacy.samples.grundsteuer_sample_data import SampleGebaeude


class TestAb1949:
    def test_if_valid_input_then_set_fields(self):
        input_data = {"isAb1949": True}

        result = Ab1949.parse_obj(input_data)

        assert result.is_ab1949 is True


class TestAbbruchverpflichtung:
    def test_if_valid_input_then_set_fields(self):
        input_data = {"hasAbbruchverpflichtung": True}

        result = Abbruchverpflichtung.parse_obj(input_data)

        assert result.has_abbruchverpflichtung is True


class TestGaragen:
    def test_if_valid_input_then_set_fields(self):
        input_data = {"hasGaragen": True}

        result = Garagen.parse_obj(input_data)

        assert result.has_garagen is True


class TestGaragenAnzahl:
    def test_if_valid_input_then_set_fields(self):
        input_data = {"anzahlGaragen": 3}

        result = GaragenAnzahl.parse_obj(input_data)

        assert result.anzahl_garagen == 3


class TestKernsaniert:
    def test_if_valid_input_then_set_fields(self):
        input_data = {"isKernsaniert": True}

        result = Kernsaniert.parse_obj(input_data)

        assert result.is_kernsaniert is True


class TestWeitereWohnraeume:
    def test_if_valid_input_then_set_fields(self):
        input_data = {"hasWeitereWohnraeume": True}

        result = WeitereWohnraeume.parse_obj(input_data)

        assert result.has_weitere_wohnraeume is True


class TestWeitereWohnraeumeDetails:
    def test_if_valid_input_then_set_fields(self):
        input_data = {"anzahl": 2, "flaeche": 42}

        result = WeitereWohnraeumeDetails.parse_obj(input_data)

        assert result.anzahl == 2
        assert result.flaeche == 42


class TestGebaeude:
    def test_if_is_ab1949_but_no_baujahr_then_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_baujahr().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_if_is_ab1949_and_baujahr_then_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_baujahr("1970").build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.baujahr.baujahr == "1970"

    def test_if_is_kernsaniert_but_no_kernsanierungsjahr_then_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_kernsanierung().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_if_is_kernsaniert_and_kernsanierungsjahr_then_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_kernsanierung("1970").build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.kernsanierungsjahr.kernsanierungsjahr == "1970"

    def test_if_has_abbruchverpflichtung_but_no_jahr_then_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_abbruchverpflichtung().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_if_has_abbruchverpflichtung_and_jahr_then_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_abbruchverpflichtung("1970").build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.abbruchverpflichtungsjahr.abbruchverpflichtungsjahr == "1970"

    def test_if_one_wohnflaeche_then_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(1).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.wohnflaechen == [1]

    def test_if_multiple_wohnflaechen_then_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(2, 3).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.wohnflaechen == [2, 3]

    def test_if_has_weitere_wohnraeume_but_no_ww_flaeche_then_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_weitere_wohnraeume().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_if_has_weitere_wohnraeume_and_ww_flaeche_then_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_weitere_wohnraeume(24, 2).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.weitere_wohnraeume_details.anzahl == 2
        assert result.weitere_wohnraeume_details.flaeche == 24

    def test_if_has_garagen_but_no_anzahl_then_raise_error(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_garagen().build()

        with pytest.raises(ValidationError):
            Gebaeude.parse_obj(gebaeude)

    def test_if_has_garagen_and_anzahl_then_parse_successfully(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_garagen(2).build()

        result = Gebaeude.parse_obj(gebaeude)

        assert result.garagen_anzahl.anzahl_garagen == 2