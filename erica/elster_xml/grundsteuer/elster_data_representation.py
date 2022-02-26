from dataclasses import dataclass
from typing import List

from erica.elster_xml.common.basic_xml import ENutzdaten, construct_basic_xml_object_representation
from erica.request_processing.erica_input.v2.grundsteuer_input import Person, GrundsteuerData, \
    Eigentuemer as EigentuemerInput


@dataclass
class EPersonData:
    Beteiligter: int
    E7404510: str
    E7404511: str

    def __init__(self, input_data: Person, person_index: int):
        self.Beteiligter = person_index + 1
        self.E7404510 = input_data.name.anrede
        self.E7404511 = input_data.name.name


@dataclass
class EEigentuemerData:
    Eigentuemer: List[EPersonData]

    def __init__(self, input_data: EigentuemerInput):
        self.Eigentuemer = []
        for index, input_eigentuemer in enumerate(input_data.person):
            new_eigentuemer = EPersonData(input_eigentuemer, index)
            self.Eigentuemer.append(new_eigentuemer)


@dataclass
class EE88:
    GW1: EEigentuemerData
    xml_attr_version: str
    xml_attr_xmlns: str

    def __init__(self, input_data: GrundsteuerData):
        self.GW1 = EEigentuemerData(input_data.eigentuemer)
        self.xml_attr_version = "2"
        self.xml_attr_xmlns = "http://finkonsens.de/elster/elstererklaerung/grundsteuerwert/e88/v2"


@dataclass
class EGrundsteuerData(ENutzdaten):
    E88: EE88

    def __init__(self, input_data: GrundsteuerData):
        self.E88 = EE88(input_data)


def get_elster_grundsteuer_data(input_data):
    return EGrundsteuerData(input_data)


def get_full_grundsteuer_data_representation(input_data):
    elster_data_representation = get_elster_grundsteuer_data(input_data)
    return construct_basic_xml_object_representation('F', "1121", elster_data_representation, "11")
