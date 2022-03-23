import pytest

from erica.erica_legacy.elster_xml.common.electronic_steuernummer import generate_electronic_aktenzeichen
from tests.erica_legacy.utils import missing_pyeric_lib


@pytest.mark.skipif(missing_pyeric_lib(), reason="skipped because of missing eric lib; see pyeric/README.md")
class TestGenerateElectronicAktenzeichen:
    def test_gernerate_electronic_aktenzeichen(self):
        result = generate_electronic_aktenzeichen("2080353038893", "NW")
        assert result == '520850353038893'
