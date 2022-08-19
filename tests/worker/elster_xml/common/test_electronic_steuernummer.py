from unittest.mock import patch

import pytest

from erica.worker.elster_xml.common.electronic_steuernummer import generate_electronic_aktenzeichen, \
    get_bufa_nr_from_steuernummer, \
    generate_electronic_steuernummer, get_bufa_nr_from_aktenzeichen
from erica.worker.pyeric.eric_errors import InvalidBufaNumberError
from worker.utils import missing_pyeric_lib


@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGetBufaNrFromSteuernummer:
    def test_if_steuernummer_given_then_return_bufa_correctly(self):
        result = get_bufa_nr_from_steuernummer("13381508159", "NW")
        assert result == "5133"

    def test_if_aktenzeichen_given_then_return_bufa_correctly(self):
        result = get_bufa_nr_from_steuernummer("2080353038893", "NW")
        assert result == "5208"

    def test_calls_steuernummer_generation(self):
        with patch("erica.worker.elster_xml.common.electronic_steuernummer.generate_electronic_steuernummer") as fun_gen_steuernummer:
            get_bufa_nr_from_steuernummer("2181508150", "BE")
            fun_gen_steuernummer.assert_called_once()


class TestGetBufaNrFromAktenzeichen:

    @pytest.mark.parametrize("bl, input_aktenzeichen, expected_bufa_nr", [
        ("NW", "2080353038893", "5208"),
        ("BW", "3100190001250002", "2831"),
        ("BY", "19869040000000012", "9198"),
        ("BE", "1687412343", "1116"),
        ("BB", "09841275756757579", "3098"),
        ("HB", "5710392627", "2457"),
        ("HH", "1605432634", "2216"),
        ("HE", "6000190000020004", "2660"),
        ("MV", "09868000600010001", "4098"),
        ("NI", "7968000600010009", "2379"),
        ("NW", "6000353012851", "5600"),
        ("RP", "70100281052000010", "2701"),
        ("SL", "01031130640290128", "1010"),
        ("SH", "9800196641", "2198"),
        ("SN", "22491703400010006", "3224"),
        ("ST", "10220000150210005", "3102"),
        ("TH", "19801005430173326", "4198")
    ])
    @pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
    def test_get_correct_bufa_number_for_correct_aktenzeichen(self, bl, input_aktenzeichen, expected_bufa_nr):

        bufa_nr = get_bufa_nr_from_aktenzeichen(input_aktenzeichen, bl)
        assert bufa_nr == expected_bufa_nr


@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGenerateElectronicAktenzeichen:
    @pytest.mark.parametrize("bl, input_stnr, expected_stnr", [
        ("NW", "2080353038893", "520850353038893"),
        ("BW", "3100190001250002", "2831400190001250002"),
        ("BY", "19869040000000012", "9198469040000000012"),
        ("BE", "1687412343", "1116087412343"),
        ("BB", "09841275756757579", "3098441275756757579"),
        ("HB", "5710392627", "2457010392627"),
        ("HH", "1605432634", "2216005432634"),
        ("HE", "6000190000020004", "2660400190000020004"),
        ("MV", "09868000600010001", "4098468000600010001"),
        ("NI", "7968000600010009", "2379468000600010009"),
        ("NW", "6000353012851", "560050353012851"),
        ("RP", "70100281052000010", "2701400281052000010"),
        ("SL", "01031130640290128", "1010431130640290128"),
        ("SH", "9800196641", "2198000196641"),
        ("SN", "22491703400010006", "3224491703400010006"),
        ("ST", "10220000150210005", "3102420000150210005"),
        ("TH", "19801005430173326", "4198401005430173326")
    ])
    def test_generate_electronic_aktenzeichen(self, bl, input_stnr, expected_stnr):
        result = generate_electronic_aktenzeichen(input_stnr, bl)
        assert result == expected_stnr


class TestGenerateElectronicSteuernummer:

    def test_empfaenger_id_correct_for_bundesland_with_one_specific_number_and_no_prepended_number(self):
        bundesland = 'BY'
        steuernummer = '18181508155'
        expected_el_steuernummer = '9181081508155'
        actual_el_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)

        assert actual_el_steuernummer == expected_el_steuernummer

    def test_empfaenger_id_correct_for_bundesland_with_two_specific_numbers_and_no_prepended_number(self):
        bundesland = 'BE'
        steuernummer = '2181508150'
        expected_el_steuernummer = '1121081508150'
        actual_el_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)

        assert actual_el_steuernummer == expected_el_steuernummer

    def test_empfaenger_id_correct_for_bundesland_with_two_specific_numbers_and_with_prepended_number(self):
        bundesland = 'HE'
        steuernummer = '01381508153'
        expected_el_steuernummer = '2613081508153'
        actual_el_steuernummer = generate_electronic_steuernummer(steuernummer, bundesland)

        assert actual_el_steuernummer == expected_el_steuernummer

    def test_if_incorrect_steuernummer_then_raise_incorrect_bufa_number_error(self):
        bundesland = 'HE'
        steuernummer = '99999999999'

        with pytest.raises(InvalidBufaNumberError):
            generate_electronic_steuernummer(steuernummer, bundesland)

    def test_if_incorrect_steuernummer_but_bufa_correct_then_raise_no_bufa_number_error(self):
        bundesland = 'HE'
        steuernummer = '01999999999'

        generate_electronic_steuernummer(steuernummer, bundesland)
