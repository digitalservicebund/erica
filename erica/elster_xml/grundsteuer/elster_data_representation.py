from dataclasses import dataclass
from typing import List, Optional

from erica.elster_xml.common.basic_xml import ENutzdaten, construct_basic_xml_object_representation
from erica.request_processing.erica_input.v2.grundsteuer_input import Person, GrundsteuerData, \
    Eigentuemer as EigentuemerInput, Anrede, Anteil


@dataclass
class EAnteil:
    E7404570: str
    E7404571: str

    def __init__(self, input_data: Anteil):
        self.E7404570 = input_data.zaehler
        self.E7404571 = input_data.nenner


@dataclass
class EPersonData:
    Beteiligter: int
    E7404510: str
    # E7404518: str
    E7404513: str
    E7404511: str
    E7404524: str
    E7404525: str
    E7404540: str
    E7404522: str
    E7404519: str
    Anteil: EAnteil
    # TODO: Eval: Order isn't important at elster anymore?
    E7404514: Optional[str] = None
    E7404527: Optional[str] = None
    E7414601: Optional[str] = None

    def __init__(self, input_data: Person, person_index: int):
        self.Beteiligter = person_index + 1
        self.E7404510 = self.elsterify_anrede(input_data.name.anrede)
        # TODO: Geburtsdatum
        self.E7404513 = input_data.name.vorname
        self.E7404511 = input_data.name.name
        self.E7404524 = input_data.adresse.strasse
        self.E7404525 = input_data.adresse.hausnummer
        self.E7404540 = input_data.adresse.plz
        self.E7404522 = input_data.adresse.ort
        self.E7404519 = input_data.steuer_id.steuer_id
        self.Anteil = EAnteil(input_data.anteil)

        # Set optional attributes
        try:
            self.E7404514 = input_data.name.titel
            self.E7404527 = input_data.adresse.postfach
            # TODO: hausnummerzusatz
            self.E7414601 = input_data.telefonnummer.telefonnummer
        except AttributeError:
            pass

    def elsterify_anrede(self, anrede_input):
        anrede_mapping = {
            Anrede.no_anrede: '01',
            Anrede.herr: '02',
            Anrede.frau: '03',
        }
        return anrede_mapping.get(anrede_input)


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
