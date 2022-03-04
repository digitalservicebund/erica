from dataclasses import dataclass
from typing import List, Optional

from erica.elster_xml.common.basic_xml_data_representation import ENutzdaten, construct_basic_xml_data_representation
from erica.request_processing.erica_input.v2.grundsteuer_input import Person, GrundsteuerData, \
    Eigentuemer as EigentuemerInput, Anrede, Anteil, Vertreter


def elsterify_anrede(anrede_input: Anrede):
    """ Converts input Anrede enum to Elster's Anrede enum """
    anrede_mapping = {
        Anrede.no_anrede: '01',
        Anrede.herr: '02',
        Anrede.frau: '03',
    }
    return anrede_mapping[anrede_input]


@dataclass
class EAnteil:
    E7404570: str
    E7404571: str

    def __init__(self, input_data: Anteil):
        self.E7404570 = input_data.zaehler
        self.E7404571 = input_data.nenner


@dataclass
class EGesetzlicherVertreter:
    E7415101: str
    E7415201: str
    E7415301: str
    E7415401: str
    E7415601: str
    E7415603: str
    E7415102: Optional[str] = None
    E7415501: Optional[int] = None
    E7415502: Optional[str] = None
    E7415602: Optional[str] = None
    E7415604: Optional[str] = None

    def __init__(self, input_data: Vertreter):
        self.E7415101 = elsterify_anrede(input_data.name.anrede)
        self.E7415201 = input_data.name.vorname
        self.E7415301 = input_data.name.name
        self.E7415401 = input_data.adresse.strasse
        self.E7415601 = input_data.adresse.plz
        self.E7415603 = input_data.adresse.ort

        # Set optional attributes
        try:
            self.E7415102 = input_data.name.titel
            self.E7415501 = input_data.adresse.hausnummer
            self.E7415502 = input_data.adresse.hausnummerzusatz
            self.E7415602 = input_data.adresse.postfach
            self.E7415604 = input_data.telefonnummer.telefonnummer
        except AttributeError:
            pass


@dataclass
class EPersonData:
    Beteiligter: int
    E7404510: str
    E7404513: str
    E7404511: str
    E7404524: str
    E7404540: str
    E7404522: str
    E7404519: str
    Anteil: EAnteil
    Ges_Vertreter: Optional[EGesetzlicherVertreter]
    E7404525: Optional[int] = None
    E7404526: Optional[str] = None
    E7404514: Optional[str] = None
    E7404527: Optional[str] = None
    E7414601: Optional[str] = None

    def __init__(self, input_data: Person, person_index: int):
        self.Beteiligter = person_index + 1
        self.E7404510 = elsterify_anrede(input_data.persoenlicheAngaben.anrede)
        self.E7404513 = input_data.persoenlicheAngaben.vorname
        self.E7404511 = input_data.persoenlicheAngaben.name
        self.E7404524 = input_data.adresse.strasse
        self.E7404540 = input_data.adresse.plz
        self.E7404522 = input_data.adresse.ort
        self.E7404519 = input_data.steuer_id.steuer_id
        self.Anteil = EAnteil(input_data.anteil)

        # Set optional attributes
        if hasattr(input_data, "vertreter") and input_data.vertreter:
            self.Ges_Vertreter = EGesetzlicherVertreter(input_data.vertreter)
        else:
            self.Ges_Vertreter = None

        try:
            self.E7404514 = input_data.persoenlicheAngaben.titel
            self.E7404527 = input_data.adresse.postfach
            self.E7404525 = input_data.adresse.hausnummer
            self.E7404526 = input_data.adresse.hausnummerzusatz
            self.E7414601 = input_data.telefonnummer.telefonnummer
        except AttributeError:
            pass


@dataclass
class EEigentumsverh:
    E7401340: str

    def __init__(self, input_data: EigentuemerInput):
        if len(input_data.person) == 1:
            self.E7401340 = "0"  # Alleineigentum
        elif len(input_data.person) == 2 and input_data.verheiratet.are_verheiratet:
            self.E7401340 = "4"  # Ehegatten / Lebenspartner
        else:
            self.E7401340 = "6"  # Bruchteilsgemeinschaft


@dataclass
class EAngFeststellung:
    E7401311: str

    def __init__(self):
        self.E7401311 = "1"  # Hauptfeststellung


@dataclass
class EGW1:
    Ang_Feststellung: EAngFeststellung
    Eigentuemer: List[EPersonData]
    Eigentumsverh: EEigentumsverh

    def __init__(self, input_data: EigentuemerInput):
        self.Ang_Feststellung = EAngFeststellung()
        self.Eigentuemer = []
        for index, input_eigentuemer in enumerate(input_data.person):
            new_eigentuemer = EPersonData(input_eigentuemer, index)
            self.Eigentuemer.append(new_eigentuemer)
        self.Eigentumsverh = EEigentumsverh(input_data)


@dataclass
class ERueckuebermittlung:
    Bescheid: str

    def __init__(self):
        self.Bescheid = '2'  # No "Bescheiddatenabholung"


@dataclass
class EVorsatz:
    Unterfallart: str
    Vorgang: str
    StNr: str
    Zeitraum: str
    AbsName: str
    AbsStr: str
    AbsPlz: str
    AbsOrt: str
    Copyright: str
    OrdNrArt: str
    Rueckuebermittlung: ERueckuebermittlung

    def __init__(self, input_data: GrundsteuerData):
        self.Unterfallart = "88"  # Grundsteuer
        self.Vorgang = "01"  # Veranlagung
        # TODO
        self.StNr = "1121081508150"
        self.Zeitraum = "2022"  # TODO require on input?
        self.AbsName = input_data.eigentuemer.person[0].persoenlicheAngaben.vorname + " " + input_data.eigentuemer.person[0].persoenlicheAngaben.name
        self.AbsStr = input_data.eigentuemer.person[0].adresse.strasse
        self.AbsPlz = input_data.eigentuemer.person[0].adresse.plz
        self.AbsOrt = input_data.eigentuemer.person[0].adresse.ort
        self.Copyright = "(C) 2022 DigitalService4Germany"
        # TODO Steuernummer or Aktenzeichen?
        self.OrdNrArt = "S"
        self.Rueckuebermittlung = ERueckuebermittlung()


@dataclass
class EE88:
    GW1: EGW1
    Vorsatz: EVorsatz
    xml_attr_version: str
    xml_attr_xmlns: str

    def __init__(self, input_data: GrundsteuerData):
        self.GW1 = EGW1(input_data.eigentuemer)
        self.Vorsatz = EVorsatz(input_data)
        self.xml_attr_version = "2"
        self.xml_attr_xmlns = "http://finkonsens.de/elster/elstererklaerung/grundsteuerwert/e88/v2"


@dataclass
class EGrundsteuerData(ENutzdaten):
    E88: EE88

    def __init__(self, input_data: GrundsteuerData):
        self.E88 = EE88(input_data)


def get_full_grundsteuer_data_representation(input_data: GrundsteuerData):
    """ Returns the full data representation of an elster XML for the Grundsteuer use case. """
    elster_data_representation = EGrundsteuerData(input_data)
    # TODO set BuFa correctly
    return construct_basic_xml_data_representation('F', "1121", elster_data_representation, "11")
