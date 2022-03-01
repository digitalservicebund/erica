import pytest
from pydantic import ValidationError

from erica.request_processing.erica_input.v2.grundsteuer_input import Eigentuemer
from tests.sample_data import get_single_person_dict


class TestEigentuemer:
    def test_if_one_person_and_verheiratet_not_given_then_do_not_raise_error(self):
        person = get_single_person_dict()
        input_data = {"person": [person]}
        Eigentuemer.parse_obj(input_data)

    def test_if_one_person_and_verheiratet_true_then_do_not_raise_error(self):
        person1 = get_single_person_dict()
        person2 = get_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {"are_verheiratet": True}}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_false_then_do_not_raise_error(self):
        person1 = get_single_person_dict()
        person2 = get_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {"are_verheiratet": False}}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_not_given_then_raise_error(self):
        person1 = get_single_person_dict()
        person2 = get_single_person_dict()
        input_data = {"person": [person1, person2]}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_given_but_are_verheiratet_not_set_then_raise_error(self):
        person1 = get_single_person_dict()
        person2 = get_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)
