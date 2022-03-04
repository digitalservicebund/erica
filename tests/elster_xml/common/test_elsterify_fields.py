import datetime

import pytest

from erica.elster_xml.common.elsterify_fields import elsterify_anrede, elsterify_date
from erica.request_processing.erica_input.v2.grundsteuer_input import Anrede


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


class TestElsterifyDate:
    def test_if_valid_date_then_return_correct_format(self):
        result = elsterify_date(datetime.date(1987, 2, 1))
        assert result == "01.02.1987"

    def test_if_invalid_date_then_raise_attribute_error(self):
        with pytest.raises(AttributeError):
            elsterify_date("INVALID")