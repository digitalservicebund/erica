import pytest
from pydantic import ValidationError

from erica.application.grundsteuer.grundsteuer_input_eigentuemer import Person, Eigentuemer
from tests.erica_legacy.samples.grundsteuer_sample_data import SamplePerson

class TestPerson:
    def test_if_snake_case_given_then_include_in_resulting_object(self):
        input_data = SamplePerson().build()
        input_data["steuer_id"] = "ID"

        result = Person.parse_obj(input_data)

        assert result.steuer_id == input_data["steuer_id"]

    def test_if_camel_case_given_then_include_in_resulting_object(self):
        input_data = SamplePerson().build()
        input_data["steuerId"] = "ID"
        input_data.pop("steuer_id")

        result = Person.parse_obj(input_data)

        assert result.steuer_id == input_data["steuerId"]

    def test_if_mixed_case_given_then_include_in_resulting_object(self):
        input_data = SamplePerson().build()
        input_data["steuerId"] = "ID"
        input_data.pop("steuer_id")

        result = Person.parse_obj(input_data)

        assert result.steuer_id == input_data["steuerId"]


class TestEigentuemer:
    def test_if_one_person_and_verheiratet_not_given_then_do_not_raise_error(self):
        person = SamplePerson().build()
        input_data = {"person": [person]}
        Eigentuemer.parse_obj(input_data)

    def test_if_one_person_and_verheiratet_true_then_raise_error(self):
        person = SamplePerson().build()
        input_data = {"person": [person], "verheiratet": True}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_one_person_and_verheiratet_false_then_raise_error(self):
        person = SamplePerson().build()
        input_data = {"person": [person], "verheiratet": False}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_true_then_do_not_raise_error(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        input_data = {"person": [person1, person2], "verheiratet": True}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_false_then_do_not_raise_error(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        input_data = {"person": [person1, person2], "verheiratet": False}
        Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_not_given_then_raise_error(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        input_data = {"person": [person1, person2]}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_two_persons_and_verheiratet_given_but_are_verheiratet_not_set_then_raise_error(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        input_data = {"person": [person1, person2], "verheiratet": {}}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_three_persons_and_verheiratet_true_then_raise_error(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        person3 = SamplePerson().build()
        input_data = {"person": [person1, person2, person3], "verheiratet": True}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)

    def test_if_three_persons_and_verheiratet_false_then_raise_error(self):
        person1 = SamplePerson().build()
        person2 = SamplePerson().build()
        person3 = SamplePerson().build()
        input_data = {"person": [person1, person2, person3], "verheiratet": False}
        with pytest.raises(ValidationError):
            Eigentuemer.parse_obj(input_data)
