from dataclasses import dataclass
from typing import List, Optional

from erica.erica_legacy.elster_xml.common.basic_xml_data_representation import ENutzdaten, construct_basic_xml_data_representation
from erica.erica_legacy.elster_xml.grundsteuer.elster_eigentuemer import EAngFeststellung, EPersonData, EEigentumsverh, \
    EEmpfangsbevollmaechtigter
from erica.erica_legacy.elster_xml.grundsteuer.elster_gebaeude import EAngWohn
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData
from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import \
    Eigentuemer as EigentuemerInput

"""
    The content of the Grundsteuer Nutzdaten XML as its data prepresentation.
    The classes are prefixed with "E" for "Elster".
"""


@dataclass
class EGW1:
    Ang_Feststellung: EAngFeststellung
    Eigentuemer: List[EPersonData]
    Eigentumsverh: EEigentumsverh
    Empfangsv: Optional[EEmpfangsbevollmaechtigter]

    def __init__(self, input_data: EigentuemerInput):
        self.Ang_Feststellung = EAngFeststellung()
        self.Eigentuemer = []
        for index, input_eigentuemer in enumerate(input_data.person):
            new_eigentuemer = EPersonData(input_eigentuemer, index)
            self.Eigentuemer.append(new_eigentuemer)
        self.Eigentumsverh = EEigentumsverh(input_data)

        if hasattr(input_data, "empfangsbevollmaechtigter") and input_data.empfangsbevollmaechtigter:
            self.Empfangsv = EEmpfangsbevollmaechtigter(input_data.empfangsbevollmaechtigter)
        else:
            self.Empfangsv = None


@dataclass
class EGW2:
    Ang_Wohn: EAngWohn

    def __init__(self, input_data: GrundsteuerData):
        self.Ang_Wohn = EAngWohn(input_data.gebaeude)


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
        self.AbsName = input_data.eigentuemer.person[0].persoenlicheAngaben.vorname + " " + \
                       input_data.eigentuemer.person[0].persoenlicheAngaben.name
        self.AbsStr = input_data.eigentuemer.person[0].adresse.strasse
        self.AbsPlz = input_data.eigentuemer.person[0].adresse.plz
        self.AbsOrt = input_data.eigentuemer.person[0].adresse.ort
        self.Copyright = "(C) 2022 DigitalService4Germany"
        # TODO Steuernummer or Aktenzeichen?
        self.OrdNrArt = "S"
        self.Rueckuebermittlung = ERueckuebermittlung()


@dataclass
class EGrundsteuerSpecifics:
    GW1: EGW1
    GW2: EGW2
    Vorsatz: EVorsatz
    xml_attr_version: str
    xml_attr_xmlns: str

    def __init__(self, input_data: GrundsteuerData):
        self.GW1 = EGW1(input_data.eigentuemer)
        self.GW2 = EGW2(input_data)
        self.Vorsatz = EVorsatz(input_data)
        self.xml_attr_version = "2"
        self.xml_attr_xmlns = "http://finkonsens.de/elster/elstererklaerung/grundsteuerwert/e88/v2"


@dataclass
class EGrundsteuerData(ENutzdaten):
    E88: EGrundsteuerSpecifics

    def __init__(self, input_data: GrundsteuerData):
        self.E88 = EGrundsteuerSpecifics(input_data)


def get_full_grundsteuer_data_representation(input_data: GrundsteuerData):
    """ Returns the full data representation of an elster XML for the Grundsteuer use case. """
    grundsteuer_elster_data_representation = EGrundsteuerData(input_data)
    # TODO set BuFa correctly
    return construct_basic_xml_data_representation(empfaenger_id='F', empfaenger_text="1121",
                                                   nutzdaten_object=grundsteuer_elster_data_representation,
                                                   nutzdaten_header_version="11")
