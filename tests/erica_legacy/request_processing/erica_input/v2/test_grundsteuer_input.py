import pytest
from pydantic import ValidationError

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input import Eigentuemer, Verheiratet, SteuerId, Person
from tests.erica_legacy.samples.grundsteuer_sample_data import get_sample_single_person_dict


class TestVerheiratet:
    def test_if_snake_case_given_then_include_in_resulting_object(self):
        input_data = {"are_verheiratet": True}

        result = Verheiratet.parse_obj(input_data)

        assert result.are_verheiratet is True

    def test_if_camel_case_given_then_include_in_resulting_object(self):
        input_data = {"areVerheiratet": True}

        result = Verheiratet.parse_obj(input_data)

        assert result.are_verheiratet is True


class TestSteuerId:
    def test_if_snake_case_given_then_include_in_resulting_object(self):
        input_data = {"steuer_id": "ID"}

        result = SteuerId.parse_obj(input_data)

        assert result.steuer_id == input_data["steuer_id"]

    def test_if_camel_case_given_then_include_in_resulting_object(self):
        input_data = {"steuerId": "ID"}

        result = SteuerId.parse_obj(input_data)

        assert result.steuer_id == input_data["steuerId"]


class TestPerson:
    def test_if_snake_case_given_then_include_in_resulting_object(self):
        input_data = get_sample_single_person_dict()
        input_data["steuer_id"]["steuer_id"] = "ID"

        result = Person.parse_obj(input_data)

        assert result.steuer_id.steuer_id == input_data["steuer_id"]["steuer_id"]

    def test_if_camel_case_given_then_include_in_resulting_object(self):
        input_data = get_sample_single_person_dict()
        input_data["steuerId"] = {"steuerId": "ID"}
        input_data.pop("steuer_id")

        result = Person.parse_obj(input_data)

        assert result.steuer_id.steuer_id == input_data["steuerId"]["steuerId"]

    def test_if_mixed_case_given_then_include_in_resulting_object(self):
        input_data = get_sample_single_person_dict()
        input_data["steuerId"] = {"steuer_id": "ID"}
        input_data.pop("steuer_id")

        result = Person.parse_obj(input_data)

        assert result.steuer_id.steuer_id == input_data["steuerId"]["steuer_id"]


class TestEigentuemer:
    def test_if_one_person_and_verheiratet_not_given_then_do_not_raise_error(self):
        person = get_sample_single_person_dict()
        input_data = {"person": [person]}
        Eigentuemer.parse_obj(input_data)

    def test_if_one_person_and_verheiratet_true_then_raise_error(self):
        person = get_sample_single_person_dict()
        input_data = {"person": [person], "verheiratet": {"are_verheiratet": True}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_one_person_and_verheiratet_false_then_raise_error(self):
        person = get_sample_single_person_dict()
        input_data = {"person": [person], "verheiratet": {"are_verheiratet": False}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_true_then_do_not_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {"are_verheiratet": True}}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_false_then_do_not_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {"are_verheiratet": False}}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_not_given_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2]}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_given_but_are_verheiratet_not_set_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2], "verheiratet": {}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_three_persons_and_verheiratet_true_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        person3 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2, person3], "verheiratet": {"are_verheiratet": True}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_three_persons_and_verheiratet_false_then_raise_error(self):
        person1 = get_sample_single_person_dict()
        person2 = get_sample_single_person_dict()
        person3 = get_sample_single_person_dict()
        input_data = {"person": [person1, person2, person3], "verheiratet": {"are_verheiratet": False}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)