from dataclasses import asdict

import xmltodict as xmltodict

from erica.elster_xml.grundsteuer.elster_data_representation import EGrundsteuerData


class CustomDict(dict):
    def __init__(self, data):
        for index, item in enumerate(data):
            if item[0].startswith('xml_attr_'):
                data[index] = (item[0].replace('xml_attr_', '@'), item[1])
            if item[0].startswith('xml_only_text'):
                data[index] = ('#text', item[1])

        super().__init__(data)


def convert_to_grundsteuer_xml(grundsteuer_object: EGrundsteuerData):
    grundsteuer_dict = asdict(grundsteuer_object, dict_factory=CustomDict)
    return xmltodict.unparse(grundsteuer_dict, pretty=True)
