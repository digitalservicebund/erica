from erica.worker.elster_xml.grundsteuer.elster_gebaeude import EWohnUnter60, EWohn60bis100, EWohnAb100, \
    EWeitereWohn, EGaragen, EAngDurchschn, EAngWohn
from erica.api.dto.grundsteuer_input_gebaeude import WeitereWohnraeumeDetails, \
    GaragenAnzahl
from tests.worker.samples.grundsteuer_sample_data import SampleGebaeude


class TestEWohnUnter60:
    def test_if_empty_input_then_retain_zeroes(self):
        flaechen = []

        result = EWohnUnter60(flaechen)

        assert result.E7403131 == 0
        assert result.E7403132 == 0

    def test_if_single_flaeche_then_set_fields(self):
        flaechen = [59]

        result = EWohnUnter60(flaechen)

        assert result.E7403131 == 1
        assert result.E7403132 == 59
        assert len(vars(result)) == 2

    def test_if_multiple_flaechen_then_calculate_fields(self):
        flaechen = [59, 1]

        result = EWohnUnter60(flaechen)

        assert result.E7403131 == 2
        assert result.E7403132 == 60


class TestEWohn60bis100:
    def test_if_empty_input_then_retain_zeroes(self):
        flaechen = []

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 0
        assert result.E7403142 == 0

    def test_if_single_flaeche_then_set_fields(self):
        flaechen = [60]

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 1
        assert result.E7403142 == 60
        assert len(vars(result)) == 2

    def test_if_multiple_flaechen_then_calculate_fields(self):
        flaechen = [99, 60]

        result = EWohn60bis100(flaechen)

        assert result.E7403141 == 2
        assert result.E7403142 == 159


class TestEWohnAb100:
    def test_if_empty_input_then_retain_zeroes(self):
        flaechen = []

        result = EWohnAb100(flaechen)

        assert result.E7403151 == 0
        assert result.E7403152 == 0

    def test_if_single_flaeche_then_set_fields(self):
        flaechen = [100]

        result = EWohnAb100(flaechen)

        assert result.E7403151 == 1
        assert result.E7403152 == 100
        assert len(vars(result)) == 2

    def test_if_multiple_flaechen_then_calculate_fields(self):
        flaechen = [100, 100]

        result = EWohnAb100(flaechen)

        assert result.E7403151 == 2
        assert result.E7403152 == 200


class TestEWeitereWohn:
    def test_if_valid_input_then_construct_from_dict_correctly(self):
        weitere_wohnraeume = WeitereWohnraeumeDetails.parse_obj({"anzahl": 2, "flaeche": 42})

        result = EWeitereWohn(weitere_wohnraeume)

        assert result.E7403121 == 2
        assert result.E7403122 == 42
        assert len(vars(result)) == 2


class TestEGaragen:
    def test_if_valid_input_then_construct_from_dict_correctly(self):
        garagen_anzahl = GaragenAnzahl.parse_obj({"anzahl_garagen": 2})

        result = EGaragen(garagen_anzahl)

        assert result.E7403171 == 2
        assert len(vars(result)) == 1


class TestEAngDurchschn:
    def test_contains_4_fields(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).parse()

        result = EAngDurchschn(gebaeude)

        assert len(vars(result)) == 4

    def test_if_wohnflaeche_under_60_then_set_others_to_none(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(59).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Wohn_unter60 == EWohnUnter60([59])
        assert result.Wohn_60bis100 is None
        assert result.Wohn_ab100 is None

    def test_if_wohnflaeche_between_60_100_then_set_others_to_none(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(99).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Wohn_unter60 is None
        assert result.Wohn_60bis100 == EWohn60bis100([99])
        assert result.Wohn_ab100 is None

    def test_if_wohnflaeche_from_100_then_set_others_to_none(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(100).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Wohn_unter60 is None
        assert result.Wohn_60bis100 is None
        assert result.Wohn_ab100 == EWohnAb100([100])

    def test_if_multiple_wohnflaechen_then_set_correct_fields(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(59, 99, 100).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Wohn_unter60 == EWohnUnter60([59])
        assert result.Wohn_60bis100 == EWohn60bis100([99])
        assert result.Wohn_ab100 == EWohnAb100([100])

    def test_if_weitere_wohnraeume_flag_true_then_set_weitere_wohnraeume(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(10).with_weitere_wohnraeume(42, 2).parse()

        result = EAngDurchschn(gebaeude)

        assert result.Weitere_Wohn is not None

    def test_if_weitere_wohnraeume_flag_false_then_not_set_weitere_wohnraeume(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(10).with_weitere_wohnraeume(42, 2).parse()
        gebaeude.weitere_wohnraeume.has_weitere_wohnraeume = False

        result = EAngDurchschn(gebaeude)

        assert result.Weitere_Wohn is None


class TestEAngWohn:
    def test_contains_6_fields(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_baujahr("1959").parse()

        result = EAngWohn(gebaeude)

        assert len(vars(result)) == 6

    def test_if_ab_1949_then_contain_baujahr_but_not_flag(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_baujahr("1959").parse()

        result = EAngWohn(gebaeude)

        assert result.E7403113 is None
        assert result.E7403114 == "1959"

    def test_if_vor_1949_then_contain_flag_but_not_baujahr(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_baujahr("1959").parse()
        gebaeude.ab1949.is_ab1949 = False

        result = EAngWohn(gebaeude)

        assert result.E7403113 == 1
        assert result.E7403114 is None

    def test_if_kernsaniert_then_contain_kernsanierungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_kernsanierung("1959").parse()

        result = EAngWohn(gebaeude)

        assert result.E7403115 == "1959"

    def test_if_not_kernsaniert_then_not_contain_kernsanierungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_kernsanierung("1959").parse()
        gebaeude.kernsaniert.is_kernsaniert = False

        result = EAngWohn(gebaeude)

        assert result.E7403115 is None

    def test_if_abbruchverpflichtung_then_contain_abbruchverpflichtungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_abbruchverpflichtung("1959").parse()

        result = EAngWohn(gebaeude)

        assert result.E7403116 == "1959"

    def test_if_no_abbruchverpflichtung_then_not_contain_abbruchverpflichtungsjahr(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_abbruchverpflichtung("1959").parse()
        gebaeude.abbruchverpflichtung.has_abbruchverpflichtung = False

        result = EAngWohn(gebaeude)

        assert result.E7403116 is None

    def test_if_garagen_then_set_anzahl(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_garagen(2).parse()

        result = EAngWohn(gebaeude)

        assert result.Garagen.E7403171 == 2

    def test_if_no_garagen_then_not_contain_garagen(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).with_garagen(2).parse()
        gebaeude.garagen.has_garagen = False

        result = EAngWohn(gebaeude)

        assert result.Garagen is None

    def test_if_valid_input_then_set_ang_durchschn(self):
        gebaeude = SampleGebaeude().with_wohnflaechen(42).parse()

        result = EAngWohn(gebaeude)

        assert result.Ang_Durchschn == EAngDurchschn(gebaeude)
