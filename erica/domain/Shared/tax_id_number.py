from collections import Counter
from stdnum.iso7064.mod_11_10 import is_valid


class TaxIdNumber(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_tax_id_number

    @classmethod
    def validate_tax_id_number(cls, tax_id_number: str) -> str:
        # must contain only digits
        if not tax_id_number.isdigit():
            raise ValueError('has to a valid idnr')
        # must contain 11 digits
        if len(tax_id_number) != 11:
            raise ValueError('has to a valid idnr')
        # one digit must exist exactly two or three times
        digits_to_check = tax_id_number[:-1]
        digit_counter = Counter(digits_to_check)
        found_repeated_digit = False
        for digit in digit_counter:
            if digit_counter[digit] > 3:
                raise ValueError('has to a valid idnr')
            if digit_counter[digit] > 1:
                if found_repeated_digit:
                    raise ValueError('has to a valid idnr')
                found_repeated_digit = True
        if not found_repeated_digit:
            raise ValueError('has to a valid idnr')
        # checksum has to be correct
        if not is_valid(tax_id_number):
            raise ValueError('has to a valid idnr')
        return tax_id_number
