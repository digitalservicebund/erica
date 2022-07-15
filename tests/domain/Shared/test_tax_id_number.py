import pytest

from erica.domain.Shared.tax_id_number import TaxIdNumber


class TestTaxIdNumberValidation:

    def test_valid_id_nr_returns_no_validation_error(self):
        tax_id_number = "17375028697"
        TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_valid_test_id_nr_returns_no_validation_error(self):
        tax_id_number = "04452397687"
        TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_if_nothing_set_then_return_validation_error(self):
        tax_id_number = ''
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)


    def test_with_letters_id_nr_returns_validation_error(self):
        tax_id_number = "A4452397687"
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_too_short_length_id_nr_returns_validation_error(self):
        tax_id_number = "123456"
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_too_long_length_id_nr_returns_validation_error(self):
        tax_id_number = "123456789109"
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_repetition_too_often_id_nr_returns_validation_error(self):
        # repeated 1 too often
        tax_id_number = "11112345678"
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_no_repetition_id_nr_returns_validation_error(self):
        tax_id_number = "01234567890"
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_too_many_repetitions_id_nr_returns_validation_error(self):
        tax_id_number = "00224567890"
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)

    def test_wrong_checksum_returns_validation_error(self):
        # 0 instead of 7
        tax_id_number = "04452397680"
        with pytest.raises(ValueError):
            TaxIdNumber.validate_tax_id_number(tax_id_number)
