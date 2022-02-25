from dataclasses import dataclass
from typing import List

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
class EGrundsteuerData:
    GW1: EEigentuemerData

    def __init__(self, input_data: GrundsteuerData):
        self.GW1 = EEigentuemerData(input_data.eigentuemer)


def get_elster_grundsteuer_data(input_data):
    return EGrundsteuerData(input_data)
