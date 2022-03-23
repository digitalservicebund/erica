from unittest.mock import patch

import pytest

from erica.erica_legacy.elster_xml.common.electronic_steuernummer import generate_electronic_aktenzeichen, get_bufa_nr
from tests.erica_legacy.utils import missing_pyeric_lib


@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGetBufaNr:
    def test_if_steuernummer_cannot_be_aktenzeichen_then_return_bufa_correctly(self):
        result = get_bufa_nr("13381508159", "NW")
        assert result == "5133"

    def test_if_steuernummer_cannot_be_aktenzeichen_then_construct_steuernummer(self):
        with patch("erica.erica_legacy.elster_xml.common.electronic_steuernummer.generate_electronic_steuernummer") as fun_gen_steuernummer:
            get_bufa_nr("2181508150", "BE")
            fun_gen_steuernummer.assert_called_once()

    def test_if_steuernummer_can_be_aktenzeichen_and_no_special_bundesland_then_return_bufa_correctly(self):
        result = get_bufa_nr("2080353038893", "NW", steuernummer_could_be_aktenzeichen=True)
        assert result == "5208"

    def test_if_steuernummer_can_be_aktenzeichen_and_no_special_bundesland_then_construct_aktenzeichen(self):
        with patch("erica.erica_legacy.elster_xml.common.electronic_steuernummer.generate_electronic_aktenzeichen") as fun_gen_aktenzeichen:
            get_bufa_nr("2080353038893", "NW", steuernummer_could_be_aktenzeichen=True)
            fun_gen_aktenzeichen.assert_called_once()

    def test_if_steuernummer_can_be_aktenzeichen_and_special_bundesland_then_return_bufa_correctly(self):
        result = get_bufa_nr("2181508150", "BE", steuernummer_could_be_aktenzeichen=True)
        assert result == "1121"

    def test_if_steuernummer_can_be_aktenzeichen_and_special_bundesland_then_construct_steuernummer(self):
        with patch("erica.erica_legacy.elster_xml.common.electronic_steuernummer.generate_electronic_steuernummer") as fun_gen_steuernummer:
            get_bufa_nr("2181508150", "BE", steuernummer_could_be_aktenzeichen=True)
            fun_gen_steuernummer.assert_called_once()


@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGenerateElectronicAktenzeichen:
    def test_gernerate_electronic_aktenzeichen(self):
        result = generate_electronic_aktenzeichen("2080353038893", "NW")
        assert result == '520850353038893'
