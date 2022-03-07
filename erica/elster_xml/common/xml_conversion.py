import copy
from dataclasses import asdict

import xmltodict as xmltodict

from erica.elster_xml.common.basic_xml_data_representation import EXml


class CustomDictParser(dict):
    """
    Parse the given object to a dict structure that xmltodict will interpret correctly.
    Attributes starting with "xml_attr_" will be interpreted as XML attributes.
    Attributes starting with "xml_text" will be treated as single text children of the XML element.
    If an attribute has the value "None" it will be not included in the resulting dict.
    The naming of the special parameters (e.g. #text) is derived form the package xmltodict.
    """
    def __init__(self, data):
        new_data = copy.deepcopy(data)
        for index, item in enumerate(data):
            if item[1] is None or item[1] == {}:
                new_data.remove(item)
            elif item[0].startswith('xml_attr_'):
                new_data[index] = (item[0].replace('xml_attr_', '@'), item[1])
            elif item[0].startswith('xml_text'):
                new_data[index] = ('#text', item[1])

        super().__init__(new_data)


def convert_object_to_xml(grundsteuer_object: EXml):
    """ Parses the given object to its XML representation. """
    grundsteuer_dict = asdict(grundsteuer_object, dict_factory=CustomDictParser)
    return xmltodict.unparse(grundsteuer_dict)
