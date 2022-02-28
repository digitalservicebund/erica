import copy
from dataclasses import asdict

import xmltodict as xmltodict

from erica.elster_xml.common.basic_xml import EXml


class CustomDictParser(dict):
    def __init__(self, data):
        new_data = copy.deepcopy(data)
        for index, item in enumerate(data):
            if item[0].startswith('xml_attr_'):
                new_data[index] = (item[0].replace('xml_attr_', '@'), item[1])
            if item[0].startswith('xml_only_text'):
                new_data[index] = ('#text', item[1])
            if item[1] is None:
                new_data.remove(item)

        super().__init__(new_data)


def convert_object_to_xml(grundsteuer_object: EXml):
    grundsteuer_dict = asdict(grundsteuer_object, dict_factory=CustomDictParser)
    return xmltodict.unparse(grundsteuer_dict, pretty=True)
