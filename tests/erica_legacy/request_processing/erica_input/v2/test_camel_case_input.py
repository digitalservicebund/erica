from erica.erica_legacy.request_processing.erica_input.v2.camel_case_input import CamelCaseInput


class DummyInput(CamelCaseInput):
    foo: str


class TestCamelCaseInput:
    def test_should_strip_leading_spaces(self):
        result = DummyInput.parse_obj({"foo": "\t  \nbar"})

        assert result.foo == "bar"

    def test_should_strip_trailing_spaces(self):
        result = DummyInput.parse_obj({"foo": "bar\t  \n"})

        assert result.foo == "bar"

    def test_should_strip_leading_and_trailing_spaces(self):
        result = DummyInput.parse_obj({"foo": "\n   \t bar\t  \n"})

        assert result.foo == "bar"

    def test_should_convert_whitespace_only_input_to_none(self):
        result = DummyInput.parse_obj({"foo": "\t  \n"})

        assert result.foo is None
