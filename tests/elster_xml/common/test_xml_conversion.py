from dataclasses import asdict, dataclass
from typing import List

import pytest

from erica.elster_xml.common.xml_conversion import CustomDictParser, convert_object_to_xml


class TestCustomDictParser:
    def test_leaves_simple_object_unchanged(self):
        @dataclass
        class SimpleObject:
            attr1: str

        input_object = SimpleObject("attrValue1")
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1"
        }

    def test_leaves_simple_nested_object_unchanged(self):
        @dataclass
        class SimpleNestedObject:
            attr1: str

        @dataclass
        class SimpleObject:
            attr1: str
            nested: SimpleNestedObject

        input_object = SimpleObject("attrValue1", SimpleNestedObject("attrValue2"))
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1",
            "nested": {
                "attr1": "attrValue2"
            }
        }

    def test_prepends_at_symbol_to_special_attributes(self):
        @dataclass
        class SimpleObject:
            attr1: str
            xml_attr_attr2: str

        input_object = SimpleObject("attrValue1", "attrValue2")
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1",
            "@attr2": "attrValue2"
        }

    def test_sets_special_attributes_to_hashtag_text(self):
        @dataclass
        class SimpleObject:
            attr1: str
            xml_text: str

        input_object = SimpleObject("attrValue1", "attrValue2")
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1",
            "#text": "attrValue2"
        }

    def test_leaves_out_attributes_set_to_none(self):
        @dataclass
        class SimpleObject:
            attr1: str
            attr2 = None

        input_object = SimpleObject("attrValue1")
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1"
        }

    def test_leaves_out_attributes_set_to_empty_dict(self):
        @dataclass
        class SimpleObject:
            attr1: str
            attr2: dict

        input_object = SimpleObject("attrValue1", {})
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1"
        }

    def test_includes_attributes_set_to_empty_string(self):
        @dataclass
        class SimpleObject:
            attr1: str
            attr2: str

        input_object = SimpleObject("attrValue1", "")
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1",
            "attr2": ""
        }

    def test_includes_attributes_set_to_empty_array(self):
        @dataclass
        class SimpleObject:
            attr1: str
            attr2: list

        input_object = SimpleObject("attrValue1", [])
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1",
            "attr2": []
        }

    def test_includes_attributes_set_to_false(self):
        @dataclass
        class SimpleObject:
            attr1: str
            attr2: bool

        input_object = SimpleObject("attrValue1", False)
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1",
            "attr2": False
        }

    def test_leaves_out_nested_objects_with_all_attributes_set_to_none(self):
        @dataclass
        class SimpleNestedObject:
            attr2 = None

        @dataclass
        class SimpleObject:
            attr1: str
            nested: SimpleNestedObject

        input_object = SimpleObject("attrValue1", SimpleNestedObject())
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "attr1": "attrValue1"
        }

    def test_converts_arrays_correctly(self):
        @dataclass
        class SimpleNestedObject:
            attr1: str

        @dataclass
        class SimpleObject:
            nested: List[SimpleNestedObject]

        input_object = SimpleObject([SimpleNestedObject("1"), SimpleNestedObject("2")])
        resulting_dict = asdict(input_object, dict_factory=CustomDictParser)
        assert resulting_dict == {
            "nested": [
                {"attr1": "1"},
                {"attr1": "2"}
            ]
        }


class TestConvertObjectToXml:
    @pytest.fixture
    def encoding_element(self):
        return '<?xml version="1.0" encoding="utf-8"?>\n'

    def test_prepends_correct_encoding_element(self, encoding_element):
        @dataclass
        class SimpleObject:
            attr1: str

        input_object = SimpleObject("attrValue1")
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.startswith(encoding_element)

    def test_returns_expected_xml_on_simple_object(self, encoding_element):
        @dataclass
        class SimpleObject:
            attr1: str

        input_object = SimpleObject("attrValue1")
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "") == "<attr1>attrValue1</attr1>"

    def test_leaves_out_empty_object_attributes(self, encoding_element):
        @dataclass
        class SimpleObject:
            attr1: str
            attr2 = None

        input_object = SimpleObject("attrValue1")
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "") == "<attr1>attrValue1</attr1>"

    def test_returns_expected_xml_on_nested_object(self, encoding_element):
        @dataclass
        class SimpleNestedObject:
            attr1: str
            attr2: str

        @dataclass
        class SimpleObject:
            nested: SimpleNestedObject

        input_object = SimpleObject(SimpleNestedObject("attrValue1", "attrValue2"))
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "").replace("\n",
                                                                   "") == "<nested><attr1>attrValue1</attr1><attr2>attrValue2</attr2></nested>"

    def test_leaves_out_empty_nested_objects(self, encoding_element):
        @dataclass
        class SimpleNestedObject:
            attr1 = None
            attr2 = None

        @dataclass
        class SimpleObject:
            attr3: str
            nested: SimpleNestedObject

        input_object = SimpleObject("attrValue3", SimpleNestedObject())
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "") == "<attr3>attrValue3</attr3>"

    def test_converts_arrays_correctly(self, encoding_element):
        @dataclass
        class SimpleNestedObject:
            attr1: str

        @dataclass
        class SimpleObject:
            nested: List[SimpleNestedObject]

        @dataclass
        class RootObject:
            root: SimpleObject

        input_object = RootObject(SimpleObject([SimpleNestedObject("1"), SimpleNestedObject("2")]))
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "").replace("\n",
                                                                   "") == "<root><nested><attr1>1</attr1></nested><nested><attr1>2</attr1></nested></root>"

    def test_leaves_out_empty_arrays(self, encoding_element):
        @dataclass
        class SimpleNestedObject:
            attr1: str

        @dataclass
        class SimpleObject:
            nested: List[SimpleNestedObject]

        @dataclass
        class RootObject:
            root: SimpleObject

        input_object = RootObject(SimpleObject([]))
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "") == "<root></root>"

    def test_sets_xml_attributes_correctly(self, encoding_element):
        @dataclass
        class SimpleObject:
            xml_attr_id: str
            attr1: str

        @dataclass
        class RootObject:
            root: SimpleObject

        input_object = RootObject(SimpleObject("ID", "attrValue1"))
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "").replace("\n",
                                                                   "") == '<root id="ID"><attr1>attrValue1</attr1></root>'

    def test_sets_direct_text_correctly(self, encoding_element):
        @dataclass
        class SimpleObject:
            xml_text: str

        @dataclass
        class RootObject:
            root: SimpleObject

        input_object = RootObject(SimpleObject("TEXT"))
        resulting_xml = convert_object_to_xml(input_object)
        assert resulting_xml.replace(encoding_element, "") == '<root>TEXT</root>'
