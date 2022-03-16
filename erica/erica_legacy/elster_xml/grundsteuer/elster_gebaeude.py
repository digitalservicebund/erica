from dataclasses import dataclass
from typing import List, Optional

from erica.erica_legacy.request_processing.erica_input.v2.grundsteuer_input_gebaeude import GaragenAnzahl, \
    WeitereWohnraeumeDetails, Gebaeude as GebaeudeInput


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
