from dataclasses import dataclass
from typing import List, Optional

from erica.elster_xml.common.basic_xml_data_representation import ENutzdaten, construct_basic_xml_data_representation
from erica.elster_xml.common.elsterify_fields import elsterify_anrede, elsterify_date
from erica.request_processing.erica_input.v2.grundsteuer_input import GrundsteuerData
from erica.request_processing.erica_input.v2.grundsteuer_input_eigentuemer import Vertreter, Anteil, Person, \
    Empfangsbevollmaechtigter, Eigentuemer as EigentuemerInput
from erica.request_processing.erica_input.v2.grundsteuer_input_gebaeude import Gebaeude as GebaeudeInput, \
    WeitereWohnraeumeDetails, GaragenAnzahl

"""
    The content of the Grundsteuer Nutzdaten XML as its data prepresentation.
    The classes are prefixed with "E" for "Elster".
"""


@dataclass
class EGaragen:
    E7403171: int  # Anzahl Garagen

    def __init__(self, garagen_anzahl: GaragenAnzahl):
        self.E7403171 = garagen_anzahl.anzahl_garagen


@dataclass
class EWohnUnter60:
    E7403131: int = 0  # Anzahl
    E7403132: int = 0  # Flaeche

    def __init__(self, flaechen: List[int]):
        for flaeche in flaechen:
            if flaeche < 60:
                self.E7403131 += 1
                self.E7403132 += flaeche


@dataclass
class EWohn60bis100:
    E7403141: int = 0
    E7403142: int = 0

    def __init__(self, flaechen: List[int]):
        for flaeche in flaechen:
            if 60 <= flaeche < 100:
                self.E7403141 += 1
                self.E7403142 += flaeche


@dataclass
class EWohnAb100:
    E7403151: int = 0
    E7403152: int = 0

    def __init__(self, flaechen: List[int]):
        for flaeche in flaechen:
            if flaeche >= 100:
                self.E7403151 += 1
                self.E7403152 += flaeche


@dataclass
class EWeitereWohn:
    E7403121: int = 0
    E7403122: int = 0

    def __init__(self, weitere_wohnraeume_details: WeitereWohnraeumeDetails):
        self.E7403121 = weitere_wohnraeume_details.anzahl
        self.E7403122 = weitere_wohnraeume_details.flaeche


@dataclass
class EAngDurchschn:
    Wohn_Unter60: Optional[EWohnUnter60] = None
    Wohn_60bis100: Optional[EWohn60bis100] = None
    Wohn_ab100: Optional[EWohnAb100] = None
    Weitere_Wohn: Optional[EWeitereWohn] = None

    def __init__(self, input_data: GebaeudeInput):
        flaechen: List[int] = []
        if input_data.wohnflaeche:
            flaechen.append(input_data.wohnflaeche.wohnflaeche)
        elif input_data.wohnflaechen:
            flaechen.append(input_data.wohnflaechen.wohnflaeche1)
            flaechen.append(input_data.wohnflaechen.wohnflaeche2)

        wohn_unter60 = EWohnUnter60(flaechen)
        if wohn_unter60.E7403131 > 0:
            self.Wohn_Unter60 = wohn_unter60

        wohn_60bis100 = EWohn60bis100(flaechen)
        if wohn_60bis100.E7403141 > 0:
            self.Wohn_60bis100 = wohn_60bis100

        wohn_ab100 = EWohnAb100(flaechen)
        if wohn_ab100.E7403151 > 0:
            self.Wohn_ab100 = wohn_ab100

        if input_data.weitere_wohnraeume.has_weitere_wohnraeume:
            self.Weitere_Wohn = EWeitereWohn(input_data.weitere_wohnraeume_details)


@dataclass
class EAngWohn:
    E7403113: Optional[int]  # vor 1949
    E7403114: Optional[str]  # Baujahr
    E7403115: Optional[str]  # Kernsanierungsjahr
    E7403116: Optional[str]  # Abbruchverpflichtungsjahr
    Garagen: Optional[EGaragen]
    Ang_Durchschn: EAngDurchschn

    def __init__(self, gebauede: GebaeudeInput):
        if gebauede.ab1949.is_ab1949:
            self.E7403113 = None
            self.E7403114 = gebauede.baujahr.baujahr
        else:
            self.E7403113 = 1
            self.E7403114 = None

        if gebauede.kernsaniert.is_kernsaniert:
            self.E7403115 = gebauede.kernsanierungsjahr.kernsanierungsjahr
        else:
            self.E7403115 = None

        if gebauede.abbruchverpflichtung.has_abbruchverpflichtung:
            self.E7403116 = gebauede.abbruchverpflichtungsjahr.abbruchverpflichtungsjahr
        else:
            self.E7403116 = None

        if gebauede.garagen.has_garagen:
            self.Garagen = EGaragen(gebauede.garagen_anzahl)
        else:
            self.Garagen = None

        self.Ang_Durchschn = EAngDurchschn(gebauede)


@dataclass
class EGW2:
    Ang_Wohn: EAngWohn

    def __init__(self, input_data: GrundsteuerData):
        self.Ang_Wohn = EAngWohn(input_data.gebaeude)


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
    E7415102: Optional[str]
    E7415501: Optional[int]
    E7415502: Optional[str]
    E7415602: Optional[str]
    E7415604: Optional[str]

    def __init__(self, input_data: Vertreter):
        self.E7415101 = elsterify_anrede(input_data.name.anrede)
        self.E7415201 = input_data.name.vorname
        self.E7415301 = input_data.name.name
        self.E7415401 = input_data.adresse.strasse
        self.E7415601 = input_data.adresse.plz
        self.E7415603 = input_data.adresse.ort

        self.E7415102 = input_data.name.titel
        self.E7415501 = input_data.adresse.hausnummer
        self.E7415502 = input_data.adresse.hausnummerzusatz
        self.E7415602 = input_data.adresse.postfach

        # input_data.telefonnummer might not be set -> handle specifically
        if hasattr(input_data, "telefonnummer") and input_data.telefonnummer:
            self.E7415604 = input_data.telefonnummer.telefonnummer
        else:
            self.E7415604 = None


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
    E7404525: Optional[str]
    E7404526: Optional[str]
    E7404514: Optional[str]
    E7404518: Optional[str]
    E7404527: Optional[str]
    E7414601: Optional[str]

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

        # input_data.vertreter might not be set -> handle specifically
        if hasattr(input_data, "vertreter") and input_data.vertreter:
            self.Ges_Vertreter = EGesetzlicherVertreter(input_data.vertreter)
        else:
            self.Ges_Vertreter = None

        self.E7404514 = input_data.persoenlicheAngaben.titel
        self.E7404518 = elsterify_date(input_data.persoenlicheAngaben.geburtsdatum)
        self.E7404527 = input_data.adresse.postfach
        self.E7404525 = input_data.adresse.hausnummer
        self.E7404526 = input_data.adresse.hausnummerzusatz

        # input_data.telefonnummer might not be set -> handle specifically
        if hasattr(input_data, "telefonnummer") and input_data.telefonnummer:
            self.E7414601 = input_data.telefonnummer.telefonnummer
        else:
            self.E7414601 = None


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
class EEmpfangsbevollmaechtigter:
    E7404610: str
    E7404614: Optional[str]
    E7404613: str
    E7404611: str
    E7404624: Optional[str]
    E7404625: Optional[str]
    E7404626: Optional[str]
    E7404640: str
    E7404627: Optional[str]
    E7404622: str
    E7412201: Optional[str]
    # TODO E7412901

    def __init__(self, input_data: Empfangsbevollmaechtigter):
        self.E7404610 = elsterify_anrede(input_data.name.anrede)
        self.E7404614 = input_data.name.titel
        self.E7404613 = input_data.name.vorname
        self.E7404611 = input_data.name.name
        self.E7404624 = input_data.adresse.strasse
        self.E7404625 = input_data.adresse.hausnummer
        self.E7404626 = input_data.adresse.hausnummerzusatz
        self.E7404640 = input_data.adresse.plz
        self.E7404627 = input_data.adresse.postfach
        self.E7404622 = input_data.adresse.ort

        # input_data.telefonnummer might not be set -> handle specifically
        if hasattr(input_data, "telefonnummer") and input_data.telefonnummer:
            self.E7412201 = input_data.telefonnummer.telefonnummer
        else:
            self.E7412201 = None


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
