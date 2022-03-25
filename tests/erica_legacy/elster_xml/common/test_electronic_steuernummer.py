from unittest.mock import patch

import pytest

from erica.erica_legacy.elster_xml.common.electronic_steuernummer import generate_electronic_aktenzeichen, get_bufa_nr, \
    generate_electronic_steuernummer
from erica.erica_legacy.pyeric.eric_errors import InvalidBufaNumberError
from tests.erica_legacy.utils import missing_pyeric_lib


@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGetBufaNr:
    def test_if_steuernummer_given_then_return_bufa_correctly(self):
        result = get_bufa_nr("13381508159", "NW")
        assert result == "5133"

    def test_if_aktenzeichen_given_then_return_bufa_correctly(self):
        result = get_bufa_nr("2080353038893", "NW")
        assert result == "5208"

    def test_calls_steuernummer_generation(self):
        with patch("erica.erica_legacy.elster_xml.common.electronic_steuernummer.generate_electronic_steuernummer") as fun_gen_steuernummer:
            get_bufa_nr("2181508150", "BE")
            fun_gen_steuernummer.assert_called_once()


@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGenerateElectronicAktenzeichen:
    def test_gernerate_electronic_aktenzeichen(self):
        result = generate_electronic_aktenzeichen("2080353038893", "NW")
        assert result == '520850353038893'


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
