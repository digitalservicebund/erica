from erica.erica_legacy.elster_xml.grundsteuer.elster_grundstueck import ELage, EMehrereGemeinden, EFlurstueck
from tests.erica_legacy.samples.grundsteuer_sample_data import SampleGrundstueck, SampleFlurstueck


class TestAdresse:
    def test_if_no_zusatz_then_parse_number_component(self):
        adresse = SampleGrundstueck().hausnummer("123").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 == "123"
        assert result.E7401126 is None

    def test_if_hausnummer_1a_then_parse_1_a(self):
        adresse = SampleGrundstueck().hausnummer("1a").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 == "1"
        assert result.E7401126 == "a"

    def test_if_hausnummersusatz_uppercase_then_parse_uppercase(self):
        adresse = SampleGrundstueck().hausnummer("0A").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 == "0"
        assert result.E7401126 == "A"

    def test_if_hausnummer_1234abc_then_parse_first_4_digits_as_nummer(self):
        adresse = SampleGrundstueck().hausnummer("1234abc").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 == "1234"
        assert result.E7401126 == "abc"

    def test_if_hausnummer_over_4_digits_then_parse_first_4_digits_as_nummer(self):
        adresse = SampleGrundstueck().hausnummer("12345").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 == "1234"
        assert result.E7401126 == "5"

    def test_if_no_hausnummer_then_should_set_none(self):
        adresse = SampleGrundstueck().hausnummer("").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 is None
        assert result.E7401126 is None

    def test_if_valid_input_then_should_assign_all_fields(self):
        adresse = SampleGrundstueck().strasse("Foostr").hausnummer("42a").zusatzangaben("hinterhaus").plz("12345").ort(
            "Berlin").parse().adresse

        result = ELage(adresse)

        assert result.E7401124 == "Foostr"
        assert result.E7401125 == "42"
        assert result.E7401126 == "a"
        assert result.E7401131 == "hinterhaus"
        assert result.E7401121 == "12345"
        assert result.E7401122 == "Berlin"

    def test_if_empty_input_then_should_assign_all_fields_none(self):
        adresse = SampleGrundstueck().typ("baureif").strasse("").hausnummer("").zusatzangaben("").plz("").ort(
            "").parse().adresse

        result = ELage(adresse)

        assert result.E7401124 is None
        assert result.E7401125 is None
        assert result.E7401126 is None
        assert result.E7401131 is None
        assert result.E7401121 is None
        assert result.E7401122 is None


class TestMehrereGemeinden:
    def test_has_one_field_with_value_one(self):
        result = EMehrereGemeinden()

        assert result.E7401190 == 1
        assert len(vars(result)) == 1


class TestEFlurstueck:
    def test_if_valid_input_then_set_fields(self):
        flurstuck = SampleFlurstueck().gemarkung("gemarky").grundbuchblattnummer("hi123").flur("c2").flurstueck_zaehler(
            42).flurstueck_nenner("24").groesse(4242).w_einheit_zaehler("1.0000").w_einheit_nenner(4).parse()

        result = EFlurstueck(flurstuck)

        assert result.E7401141 == "gemarky"
        assert result.E7401142 == "hi123"
        assert result.E7401143 == "c2"
        assert result.E7401144 == 42
        assert result.E7401145 == "24"
        assert result.E7411001 == 4242
        assert result.E7410702 == "1.0000"
        assert result.E7410703 == 4

    def test_if_largest_groesse_then_parsed_identically(self):
        flurstuck = SampleFlurstueck().groesse(999999999999999).parse()

        result = EFlurstueck(flurstuck)

        assert result.E7411001 == 999999999999999
