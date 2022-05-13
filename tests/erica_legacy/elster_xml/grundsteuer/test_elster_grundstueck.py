from erica.erica_legacy.elster_xml.common.elsterify_fields import elsterify_grundstuecksart, \
    elsterify_wirtschaftliche_einheit_zaehler
from erica.erica_legacy.elster_xml.grundsteuer.elster_grundstueck import ELage, EMehrereGemeinden, EFlurstueck, \
    EAngFlaeche, EEntwZust, EAngGrund, EAngGrundstuecksart
from erica.application.grundsteuer.grundsteuer_input_grundstueck  import Grundstuecksart
from tests.erica_legacy.samples.grundsteuer_sample_data import SampleGrundstueck, SampleFlurstueck


class TestELage:
    def test_if_no_zusatz_then_parse_number_component(self):
        adresse = SampleGrundstueck().hausnummer("123").hausnummerzusatz(None).parse().adresse

        result = ELage(adresse)

        assert result.E7401125 == "123"
        assert result.E7401126 is None

    def test_if_hausnummer_1a_then_parse_1_a(self):
        adresse = SampleGrundstueck().hausnummer("1").hausnummerzusatz("a").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 == "1"
        assert result.E7401126 == "a"

    def test_if_no_hausnummer_then_should_set_none(self):
        adresse = SampleGrundstueck().hausnummer("").hausnummerzusatz("").parse().adresse

        result = ELage(adresse)

        assert result.E7401125 is None
        assert result.E7401126 is None

    def test_if_valid_input_then_should_assign_all_fields(self):
        adresse = SampleGrundstueck().strasse("Foostr").hausnummer("42").hausnummerzusatz("a").zusatzangaben("hinterhaus").plz("12345").ort(
            "Berlin").parse().adresse

        result = ELage(adresse)

        assert result.E7401124 == "Foostr"
        assert result.E7401125 == "42"
        assert result.E7401126 == "a"
        assert result.E7401131 == "hinterhaus"
        assert result.E7401121 == "12345"
        assert result.E7401122 == "Berlin"
        assert len(vars(result)) == 6

    def test_if_empty_input_then_should_assign_all_fields_none(self):
        adresse = SampleGrundstueck().typ("baureif").strasse("").hausnummer("").hausnummerzusatz("").zusatzangaben("").plz("").ort(
            "").parse().adresse

        result = ELage(adresse)

        assert result.E7401124 is None
        assert result.E7401125 is None
        assert result.E7401126 is None
        assert result.E7401131 is None
        assert result.E7401121 is None
        assert result.E7401122 is None
        assert len(vars(result)) == 6


class TestEAngGrundstuecksart:
    def test_if_valid_input_then_should_assign_field(self):
        result = EAngGrundstuecksart(Grundstuecksart.einfamilienhaus)

        assert result.E7401322 == elsterify_grundstuecksart(Grundstuecksart.einfamilienhaus)
        assert len(vars(result)) == 1


class TestEMehrereGemeinden:
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
        assert result.E7410702 == elsterify_wirtschaftliche_einheit_zaehler("1.0000")
        assert result.E7410703 == 4
        assert result.E7410704 == 1
        assert len(vars(result)) == 9

    def test_if_largest_groesse_then_parsed_identically(self):
        flurstuck = SampleFlurstueck().groesse(999999999999999).parse()

        result = EFlurstueck(flurstuck)

        assert result.E7411001 == 999999999999999


class TestEEntwZust:
    def test_if_bauerwartungsland_should_set_1(self):
        result = EEntwZust("bauerwartungsland")

        assert result.E7403051 == 1

    def test_if_rohbauland_should_set_2(self):
        result = EEntwZust("rohbauland")

        assert result.E7403051 == 2


class TestEAngGrund:
    def test_if_valid_input_then_set_fields_correctly(self):
        grundstueck = SampleGrundstueck().abweichende_enwticklung("rohbauland").parse()

        result = EAngGrund(grundstueck)

        assert result.Ang_Flaeche == EAngFlaeche(grundstueck)
        assert result.Entw_Zust == EEntwZust(grundstueck.abweichende_entwicklung)
        assert len(vars(result)) == 2

    def test_if_no_abweichende_entwicklung_then_set_field_none(self):
        grundstueck = SampleGrundstueck().parse()

        result = EAngGrund(grundstueck)

        assert result.Ang_Flaeche == EAngFlaeche(grundstueck)
        assert result.Entw_Zust is None
        assert len(vars(result)) == 2


class TestEAngFlaeche:
    def test_if_one_flurstueck_whole_then_calculate_correctly(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).w_einheit_zaehler("1.0000").w_einheit_nenner(1).parse()
        grundstueck = SampleGrundstueck().bodenrichtwert("422,99").flurstuck(flurstueck1).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 1000
        assert result.E7403011 == "422,99"
        assert len(vars(result)) == 2

    def test_if_one_flurstueck_partial_then_calculate_correctly(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).w_einheit_zaehler("1.0000").w_einheit_nenner(2).parse()
        grundstueck = SampleGrundstueck().flurstuck(flurstueck1).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 500

    def test_if_zaehler_with_nonzero_fraction_then_calculate_correctly(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).w_einheit_zaehler("1.2345").w_einheit_nenner(2).parse()
        grundstueck = SampleGrundstueck().flurstuck(flurstueck1).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 617

    def test_if_zaehler_fraction_less_than_half_result_then_round_down_to_int(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).w_einheit_zaehler("1.0000").w_einheit_nenner(3).parse()
        grundstueck = SampleGrundstueck().flurstuck(flurstueck1).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 333

    def test_if_zaehler_fraction_greater_than_half_result_then_round_down_to_int(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).w_einheit_zaehler("2.0000").w_einheit_nenner(3).parse()
        grundstueck = SampleGrundstueck().flurstuck(flurstueck1).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 666

    def test_if_two_flurstuecke_then_calculate_sum(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).w_einheit_zaehler("1.0000").w_einheit_nenner(1).parse()
        flurstueck2 = SampleFlurstueck().groesse(500).w_einheit_zaehler("2.0000").w_einheit_nenner(4).parse()

        grundstueck = SampleGrundstueck().flurstuck(flurstueck1).flurstuck(flurstueck2).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 1250

    def test_if_two_flurstuecke_without_explicit_values_then_calculate_sum_from_defaults(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).parse()
        flurstueck2 = SampleFlurstueck().groesse(500).parse()

        grundstueck = SampleGrundstueck().flurstuck(flurstueck1).flurstuck(flurstueck2).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 1500

    def test_if_two_flurstuecke_only_one_with_explicit_values_then_calculate_sum_from_defaults(self):
        flurstueck1 = SampleFlurstueck().groesse(1000).w_einheit_zaehler("1.0000").w_einheit_nenner(4).parse()
        flurstueck2 = SampleFlurstueck().groesse(500).parse()

        grundstueck = SampleGrundstueck().flurstuck(flurstueck1).flurstuck(flurstueck2).parse()

        result = EAngFlaeche(grundstueck)

        assert result.E7403010 == 750
